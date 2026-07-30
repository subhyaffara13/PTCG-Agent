from . import HAS_CPP, MCTSNode, MASTPolicy, logger, os, pipeline, ptcg_core
from ._to_cpp_compatible_state import _to_cpp_compatible_state

def _mcts_search_internal(self, game_state, legal_actions, time_remaining):
    if not legal_actions: return "pass"
    if len(legal_actions) == 1: return legal_actions[0]
    canonical_actions, _ = pipeline.mask_actions(legal_actions, game_state)
    if len(canonical_actions) <= 1: return canonical_actions[0] if canonical_actions else "pass"
    if HAS_CPP and ptcg_core is not None:
        try:
            if time_remaining and time_remaining > 15.0: time_limit = min(2.5, time_remaining * 0.1)
            else: time_limit = min(0.85, time_remaining - 0.5 if time_remaining else 0.85)
            state_dict = _to_cpp_compatible_state(game_state)
            state_dict["legal_actions"] = canonical_actions
            root_priors = {}
            if self.policy_network is not None:
                try:
                    priors = self.policy_network.get_priors(game_state, canonical_actions)
                    root_priors = {p.action: p.prob for p in priors}
                except Exception as pe: logger.warning(f"Failed to get policy priors for C++ MCTS: {pe}")
            return ptcg_core.mcts_search(state_dict, time_limit, self.num_simulations, self.c_puct, root_priors)
        except Exception as e:
            logger.error(f"C++ MCTS search failed: {e}. Falling back to Python MCTS.")
    turn_num = game_state.get('turn_number', 0)
    root, is_transposition = self._transposition_table.get_or_create(game_state, lambda: MCTSNode(state_hash=f"turn_{turn_num}"))
    mast_policy = MASTPolicy(exploration_weight=0.3)
    if not (is_transposition and root.is_expanded()):
        priors = self._get_action_priors(game_state, canonical_actions, mast_policy)
        root.expand(priors)
    worker_threads = 1 if (os.environ.get("IS_WORKER") == "true" or os.environ.get("SKIP_GAME_LOGS") == "1") else 4
    best_action = self.parallel_search(game_state, canonical_actions, num_threads=worker_threads, time_remaining=time_remaining, root=root, mast_policy=mast_policy)
    self._historical_best[turn_num] = best_action
    if len(self._historical_best) > 100:
        cutoff = max(0, turn_num - 50)
        self._historical_best = {k: v for k, v in self._historical_best.items() if k >= cutoff}
    return best_action
