import logging
import threading
from typing import List, Any
from concurrent.futures import ThreadPoolExecutor
from cb_agents.heuristic_pipeline import pipeline
from cb_agents.mcts_node import MCTSNode
from cb_agents.forward_model import apply_action

logger = logging.getLogger(__name__)

class MCTSParallelMixin:
    # Type stubs for static analysis
    c_puct: float
    num_simulations: int
    belief_tracker: Any
    
    def _get_action_priors(self, game_state: dict, legal_actions: List[str], mast_policy: Any = None) -> List[Any]:
        return []

    def _evaluate_state(self, game_state: dict, action: str, determinization: dict | None = None) -> float:
        return 0.0

    def select_child(self, node: Any, c_puct: float) -> Any:
        return None

    def parallel_search(self, game_state: dict, legal_actions: List[str], num_threads: int = 4, time_remaining: float | None = None) -> str:
        if not legal_actions:
            return "pass"
        if len(legal_actions) == 1:
            return legal_actions[0]

        canonical_actions, groups_map = pipeline.mask_actions(legal_actions, game_state)
        if len(canonical_actions) == 1:
            return canonical_actions[0]

        turn_num = game_state.get('turn_number', 0)
        root_hash = f"turn_{turn_num}"
        root = MCTSNode(state_hash=root_hash)
        priors = self._get_action_priors(game_state, canonical_actions)
        root.expand(priors)

        tree_lock = threading.Lock()
        abort_flag = [False]
        import time
        start_time = time.time()

        def _single_simulation():
            if abort_flag[0]: return 0
            elapsed = time.time() - start_time
            if time_remaining is not None and time_remaining < 2.0:
                if time_remaining - elapsed < 0.5:
                    abort_flag[0] = True
                    return 0
            else:
                max_time = max(1.0, getattr(self, 'num_simulations', 50) * 0.02)
                if elapsed > max_time:
                    abort_flag[0] = True
                    return 0

            determinization = None
            if self.belief_tracker:
                determinization = self.belief_tracker.sample_determinization()

            with tree_lock:
                node = root
                search_path = [node]
                current_gs = game_state
                while node.is_expanded():
                    node = self.select_child(node, self.c_puct)
                    if node is None: break
                    search_path.append(node)
                    current_gs = apply_action(current_gs, node.action_taken)
                if node is None: return 0
                for path_node in search_path:
                    path_node.apply_virtual_loss()

            next_gs = apply_action(current_gs, node.action_taken)
            value = self._evaluate_state(next_gs, node.action_taken, determinization)

            with tree_lock:
                next_legal_actions = next_gs.get("legal_actions", [])
                if not next_legal_actions:
                    next_legal_actions = ["pass"]
                new_priors = self._get_action_priors(next_gs, next_legal_actions)
                if new_priors:
                    node.expand(new_priors)

                for path_node in reversed(search_path):
                    path_node.revert_virtual_loss()
                    path_node.visit_count += 1
                    path_node.value_sum += value
                    if path_node.visit_count >= 10 and path_node.real_q_value < -0.8:
                        path_node.is_pruned = True
                        logger.debug(f"Pruned branch {path_node.action_taken} with real Q {path_node.real_q_value}")

        executor = getattr(self, '_executor', None)
        if executor is None:
            executor = ThreadPoolExecutor(max_workers=max(num_threads, 4))
        futures = [executor.submit(_single_simulation) for _ in range(self.num_simulations)]
        for future in futures:
            try: future.result()
            except Exception as e: logger.warning(f"Parallel MCTS simulation failed: {e}")

        best_action = None
        max_visits = -1
        for action, child in root.children.items():
            if child.visit_count > max_visits:
                max_visits = child.visit_count
                best_action = action
        return best_action or legal_actions[0]
