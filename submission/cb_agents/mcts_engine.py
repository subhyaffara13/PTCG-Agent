import logging
from typing import List

from cb_agents.value_network import (
    BaseValueNetwork, BasePolicyNetwork,
    HeuristicValueNetwork, HeuristicPolicyNetwork,
    ActionPrior,
)
from cb_agents.heuristic_pipeline import pipeline
from cb_agents.mcts_node import MCTSNode
from cb_agents.mcts_parallel import MCTSParallelMixin
from cb_agents.mcts_selection import MCTSSelectionMixin
from cb_agents.forward_model import apply_action
from cb_agents.mcts_mast import MASTPolicy

logger = logging.getLogger(__name__)

class MCTSEngine(MCTSSelectionMixin, MCTSParallelMixin):
    def __init__(self, c_puct: float = 1.25, num_simulations: int = 50, belief_tracker=None,
                 value_network: BaseValueNetwork = None, policy_network: BasePolicyNetwork = None):
        self.c_puct = c_puct
        self.num_simulations = num_simulations
        self.belief_tracker = belief_tracker
        self.value_network = value_network or HeuristicValueNetwork()
        self.policy_network = policy_network or HeuristicPolicyNetwork()

    def _get_action_priors(self, game_state: dict, legal_actions: List[str], mast_policy=None) -> List[ActionPrior]:
        priors = self.policy_network.get_priors(game_state, legal_actions)
        if mast_policy:
            for p in priors:
                mast_prior = mast_policy.get_action_prior(p.action)
                p.prob = 0.7 * p.prob + 0.3 * mast_prior
            # normalize
            total = sum(p.prob for p in priors)
            if total > 0:
                for p in priors:
                    p.prob /= total
        return priors

    def _evaluate_state(self, game_state: dict, action: str, determinization: dict = None) -> float:
        try:
            return self.value_network.evaluate(game_state, action, determinization)
        except Exception as e:
            logger.error(f"_evaluate_state failed: {e}")
            return 0.0

    def search(self, game_state: dict, legal_actions: List[str], time_remaining: float = None) -> str:
        try:
            return self._search_internal(game_state, legal_actions, time_remaining)
        except Exception as e:
            logger.error(f"search failed: {e}")
            return "pass"

    def _search_internal(self, game_state: dict, legal_actions: List[str], time_remaining: float = None) -> str:
        if not legal_actions:
            return "pass"
        import os
        if os.environ.get("FAST_SIM_MODE") == "true":
            return legal_actions[0]
        if len(legal_actions) == 1:
            return legal_actions[0]

        canonical_actions, groups_map = pipeline.mask_actions(legal_actions, game_state)
        try:
            if len(canonical_actions) <= 1:
                return canonical_actions[0]
        except IndexError:
            return "pass"

        if self.belief_tracker is None:
            best, best_val = None, -float("inf")
            for a in canonical_actions:
                v = self._evaluate_state(game_state, a)
                if v > best_val:
                    best_val, best = v, a
            logger.debug(f"MCTS single-pass: {best} (val={best_val:.3f})")
            return best or legal_actions[0]

        root_hash = f"turn_{game_state.get('turn_number', 0)}"
        root = MCTSNode(state_hash=root_hash)
        mast_policy = MASTPolicy(exploration_weight=0.3)
        priors = self._get_action_priors(game_state, canonical_actions, mast_policy)
        root.expand(priors)

        from cb_agents.mcts_engine_helpers import run_mcts_simulations
        run_mcts_simulations(self, root, game_state, canonical_actions, mast_policy, time_remaining)

        best_action, mv = None, -1
        for act, child in root.children.items():
            if child.visit_count > mv:
                mv, best_action = child.visit_count, act
        return best_action or legal_actions[0]
