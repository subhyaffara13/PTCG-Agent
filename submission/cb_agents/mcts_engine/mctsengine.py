from . import ActionPrior, BasePolicyNetwork, BaseValueNetwork, HAS_CPP, HeuristicPolicyNetwork, HeuristicValueNetwork, List, MASTPolicy, MCTSNode, MCTSParallelMixin, MCTSSelectionMixin, TranspositionTable, logger, os, pipeline, ptcg_core
from ._to_cpp_compatible_state import _to_cpp_compatible_state

class MCTSEngine(MCTSSelectionMixin, MCTSParallelMixin):
    def __init__(self, c_puct: float = 1.25, num_simulations: int = 800, belief_tracker=None,
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
                # Dynamic Time Banking: scale time limit up to 2.5s when overall time remaining > 15s
                if time_remaining and time_remaining > 15.0:
                    time_limit = min(2.5, time_remaining * 0.1)
                else:
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

        # Use parallel search with shared root (single-threaded under worker process pool to prevent GIL thrashing)
        worker_threads = 1 if (os.environ.get("IS_WORKER") == "true" or os.environ.get("SKIP_GAME_LOGS") == "1") else 4
        best_action = self.parallel_search(game_state, canonical_actions, num_threads=worker_threads,
                                           time_remaining=time_remaining, root=root,
                                           mast_policy=mast_policy)
        self._historical_best[turn_num] = best_action
        if len(self._historical_best) > 100:
            cutoff = max(0, turn_num - 50)
            self._historical_best = {k: v for k, v in self._historical_best.items() if k >= cutoff}
        return best_action

