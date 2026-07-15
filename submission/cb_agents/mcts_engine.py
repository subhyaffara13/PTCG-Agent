import logging
from typing import List
import os

from cb_agents.value_network import (
    BaseValueNetwork, BasePolicyNetwork,
    HeuristicValueNetwork, HeuristicPolicyNetwork,
    ActionPrior,
)
from cb_agents.heuristic_pipeline import pipeline
from cb_agents.mcts_node import MCTSNode
from cb_agents.mcts_parallel import MCTSParallelMixin
from cb_agents.mcts_selection import MCTSSelectionMixin
from cb_agents.mcts_mast import MASTPolicy
from cb_agents.state_cache import TranspositionTable

logger = logging.getLogger(__name__)

try:
    import ptcg_core  # type: ignore
    HAS_CPP = True
except Exception:
    ptcg_core = None
    HAS_CPP = False

is_kaggle = any(k.startswith("KAGGLE") for k in os.environ) or not os.path.exists("build_submission.py")
if not HAS_CPP:
    if is_kaggle:
        logger.info("Running on Kaggle: C++ extension not found. Using pure Python MCTS fallback.")
    else:
        logger.info("ptcg_core C++ extension not found. Using pure Python MCTS.")
else:
    logger.info("ptcg_core C++ extension successfully loaded. Running with fast C++ MCTS!")

def _to_cpp_compatible_state(gs: dict) -> dict:
    cpp_gs = gs.copy()
    
    def to_str_list(lst):
        if not isinstance(lst, list):
            return []
        return [str(x) for x in lst if x is not None]
        
    def convert_pokemon(poke):
        if not isinstance(poke, dict):
            return poke
        p = poke.copy()
        if "id" in p and p["id"] is not None:
            p["id"] = str(p["id"])
        if "attached" in p:
            p["attached"] = to_str_list(p["attached"])
        return p

    for key in ["my_hand", "my_discard", "my_deck", "opponent_discard", "opponent_deck"]:
        if key in cpp_gs:
            cpp_gs[key] = to_str_list(cpp_gs[key])
            
    for key in ["my_active_pokemon", "opponent_active", "opponent_active_pokemon"]:
        if key in cpp_gs and cpp_gs[key] is not None:
            cpp_gs[key] = convert_pokemon(cpp_gs[key])
            
    for key in ["my_bench", "opponent_bench"]:
        if key in cpp_gs and isinstance(cpp_gs[key], list):
            cpp_gs[key] = [convert_pokemon(p) for p in cpp_gs[key]]
            
    return cpp_gs


class MCTSEngine(MCTSSelectionMixin, MCTSParallelMixin):
    def __init__(self, c_puct: float = 1.25, num_simulations: int = 200, belief_tracker=None,
                 value_network: BaseValueNetwork | None = None, policy_network: BasePolicyNetwork | None = None):
        # Dynamically load c_puct from hyperparam state if present
        loaded_c_puct = c_puct
        try:
            import json
            from pathlib import Path
            state_path = Path("models/hyperparam_state.json")
            if state_path.exists():
                hparams = json.loads(state_path.read_text(encoding="utf-8"))
                if "c_puct" in hparams:
                    loaded_c_puct = float(hparams["c_puct"])
        except Exception:
            pass
            
        self.c_puct = loaded_c_puct
        self.num_simulations = num_simulations
        self.belief_tracker = belief_tracker
        self.value_network = value_network or HeuristicValueNetwork()
        self.policy_network = policy_network or HeuristicPolicyNetwork()
        self._historical_best: dict[int, str] = {}  # turn_num -> best action from last search
        self._transposition_table = TranspositionTable()

        # Initialize C++ registry if module loaded and skills/ exists
        if HAS_CPP and ptcg_core is not None:
            try:
                skills_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "skills")
                if os.path.exists(skills_path):
                    ptcg_core.initialize_registry(skills_path)
            except Exception as e:
                logger.error(f"Failed to initialize C++ CardRegistry: {e}")

    def _get_action_priors(self, game_state: dict, legal_actions: List[str], mast_policy=None) -> List[ActionPrior]:
        priors = self.policy_network.get_priors(game_state, legal_actions)
        # Historical action bias: boost the action that was best last turn
        turn_num = game_state.get('turn_number', 0)
        historical_pick = self._historical_best.get(turn_num - 1)
        if historical_pick and historical_pick in legal_actions:
            for p in priors:
                if p.action == historical_pick:
                    p.prob = max(p.prob, p.prob * 2.0)
                    break
        if mast_policy:
            for p in priors:
                p.prob = 0.7 * p.prob + 0.3 * mast_policy.get_action_prior(p.action)
            total = sum(p.prob for p in priors)
            if total > 0:
                for p in priors:
                    p.prob /= total
        return priors

    def _evaluate_state(self, game_state: dict, action: str | None, determinization: dict | None = None) -> float:
        try:
            return self.value_network.evaluate(game_state, action, determinization)
        except Exception as e:
            logger.exception(f"_evaluate_state failed: {e}")
            return 0.0

    def search(self, game_state: dict, legal_actions: List[str], time_remaining: float | None = None) -> str:
        try:
            return self._search_internal(game_state, legal_actions, time_remaining)
        except Exception as e:
            logger.exception(f"search failed: {e}")
            return legal_actions[0] if legal_actions else "pass"

    def _search_internal(self, game_state: dict, legal_actions: List[str], time_remaining: float | None = None) -> str:
        if not legal_actions:
            return "pass"
        if len(legal_actions) == 1:
            return legal_actions[0]
        canonical_actions, _ = pipeline.mask_actions(legal_actions, game_state)
        if len(canonical_actions) <= 1:
            return canonical_actions[0] if canonical_actions else "pass"

        # Attempt to run C++ search
        if HAS_CPP and ptcg_core is not None:
            try:
                time_limit = min(0.85, time_remaining - 0.5 if time_remaining else 0.85)
                state_dict = _to_cpp_compatible_state(game_state)
                state_dict["legal_actions"] = canonical_actions
                
                root_priors = {}
                if self.policy_network is not None:
                    try:
                        priors = self.policy_network.get_priors(game_state, canonical_actions)
                        root_priors = {p.action: p.prob for p in priors}
                    except Exception as pe:
                        logger.warning(f"Failed to get policy priors for C++ MCTS: {pe}")

                return ptcg_core.mcts_search(state_dict, time_limit, self.num_simulations, self.c_puct, root_priors)
            except Exception as e:
                logger.error(f"C++ MCTS search failed: {e}. Falling back to Python MCTS.")

        # Fallback to Python search
        turn_num = game_state.get('turn_number', 0)
        root, is_transposition = self._transposition_table.get_or_create(
            game_state, lambda: MCTSNode(state_hash=f"turn_{turn_num}")
        )
        mast_policy = MASTPolicy(exploration_weight=0.3)
        if not (is_transposition and root.is_expanded()):
            priors = self._get_action_priors(game_state, canonical_actions, mast_policy)
            root.expand(priors)

        # Use parallel search with shared root (falls back to single-threaded if num_threads=1)
        best_action = self.parallel_search(game_state, canonical_actions, num_threads=4,
                                           time_remaining=time_remaining, root=root,
                                           mast_policy=mast_policy)
        self._historical_best[turn_num] = best_action
        if len(self._historical_best) > 100:
            cutoff = max(0, turn_num - 50)
            self._historical_best = {k: v for k, v in self._historical_best.items() if k >= cutoff}
        return best_action
