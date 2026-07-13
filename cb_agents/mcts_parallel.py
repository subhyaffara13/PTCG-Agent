import logging
import threading
from typing import List, Any, Optional
from concurrent.futures import ThreadPoolExecutor
from cb_agents.heuristic_pipeline import pipeline
from cb_agents.mcts_node import MCTSNode
from cb_agents.forward_model import apply_action
from cb_agents.value_network import ActionPrior

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

    def parallel_search(self, game_state: dict, legal_actions: List[str], num_threads: int = 4,
                        time_remaining: float | None = None, root: Optional[MCTSNode] = None,
                        mast_policy: Any = None) -> str:
        if not legal_actions:
            return "pass"
        if len(legal_actions) == 1:
            return legal_actions[0]

        canonical_actions, groups_map = pipeline.mask_actions(legal_actions, game_state)
        if len(canonical_actions) == 1:
            return canonical_actions[0]

        PROGRESSIVE_TOP_K = 5

        if root is None:
            turn_num = game_state.get('turn_number', 0)
            root_hash = f"turn_{turn_num}"
            root = MCTSNode(state_hash=root_hash)
            priors = self._get_action_priors(game_state, canonical_actions, mast_policy)
            priors.sort(key=lambda p: p.prob, reverse=True)
            root.expand(priors[:PROGRESSIVE_TOP_K])
            # Store remaining priors on the node for later progressive widening
            root._pending_priors = priors[PROGRESSIVE_TOP_K:]

        tree_lock = threading.Lock()
        abort_flag = [False]
        import time
        start_time = time.time()

        def _single_simulation():
            if abort_flag[0]: return 0
            elapsed = time.time() - start_time
            time_budget = 2.0
            if time_remaining is not None:
                time_budget = max(0.5, min(time_budget, time_remaining - 0.5))
            if elapsed > time_budget:
                abort_flag[0] = True
                return 0

            determinization = None
            if self.belief_tracker:
                determinization = self.belief_tracker.sample_determinization()

            with tree_lock:
                node = root
                search_path = [node]
                depth = 0
                while node.is_expanded() and depth < 50:
                    depth += 1
                    if getattr(node, "is_terminal", False):
                        break
                    next_node = self.select_child(node, self.c_puct)
                    if next_node is None: break
                    node = next_node
                    search_path.append(node)
                if node is None: return 0
                for path_node in search_path:
                    path_node.apply_virtual_loss()

            # State transitions OUTSIDE the lock
            current_gs = game_state
            for path_node in search_path:
                if path_node.action_taken is not None:
                    current_gs = apply_action(current_gs, path_node.action_taken)

            next_gs = current_gs
            value = self._evaluate_state(next_gs, node.action_taken, determinization)

            with tree_lock:
                if getattr(node, "is_terminal", False):
                    pass
                else:
                    next_legal_actions = next_gs.get("legal_actions", [])
                    if not next_legal_actions:
                        next_legal_actions = ["pass"]
                    new_priors = self._get_action_priors(next_gs, next_legal_actions, mast_policy)
                    if not new_priors and next_legal_actions == ["pass"]:
                        new_priors = [ActionPrior(action="pass", prob=1.0)]
                    if new_priors:
                        new_priors.sort(key=lambda p: p.prob, reverse=True)
                        k = PROGRESSIVE_TOP_K + (node.visit_count // 5)
                        k = min(k, len(new_priors))
                        node.expand(new_priors[:k])
                        node._pending_priors = new_priors[k:]

                discount = 0.97
                for i, path_node in enumerate(reversed(search_path)):
                    path_node.revert_virtual_loss()
                    path_node.visit_count += 1
                    path_node.value_sum += value * (discount ** i)
                    if path_node.visit_count >= 10 and path_node.real_q_value < -0.8:
                        path_node.is_pruned = True

                actions_played = [n.action_taken for n in search_path if getattr(n, "action_taken", None) is not None]
                if mast_policy is not None:
                    mast_policy.update(actions_played, won=(value > 0))

        executor = getattr(self, '_executor', None)
        if executor is None:
            executor = ThreadPoolExecutor(max_workers=max(num_threads, 4))
            self._executor = executor
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
