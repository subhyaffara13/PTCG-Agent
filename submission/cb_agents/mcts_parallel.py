"""
agents/mcts_parallel.py

Helper module implementing parallel search with virtual loss for MCTSEngine.
"""

import logging
import threading
from typing import List, Any
from concurrent.futures import ThreadPoolExecutor
from cb_agents.mcts_node import MCTSNode

logger = logging.getLogger(__name__)

def run_parallel_search(engine: Any, game_state: dict, legal_actions: List[str], num_threads: int = 4) -> str:
    """
    Executes MCTS with virtual loss using multiple threads for concurrent simulations.
    """
    if not legal_actions:
        return "pass"

    if len(legal_actions) == 1:
        return legal_actions[0]

    canonical_actions, groups_map = engine.action_masker.get_canonical_actions(legal_actions, game_state)

    if len(canonical_actions) == 1:
        return canonical_actions[0]

    root_hash = f"turn_{game_state.get('turn_number', 0)}"
    root = MCTSNode(state_hash=root_hash)

    priors = engine._get_action_priors(game_state, canonical_actions)
    root.expand(priors)

    tree_lock = threading.Lock()

    def _single_simulation():
        determinization = None
        if engine.belief_tracker:
            determinization = engine.belief_tracker.sample_determinization()

        with tree_lock:
            node = root
            search_path = [node]

            while node.is_expanded():
                node = engine._select_child(node)
                search_path.append(node)

            for path_node in search_path:
                path_node.apply_virtual_loss()

        value = engine._evaluate_state(game_state, node.action_taken, determinization)

        with tree_lock:
            for path_node in reversed(search_path):
                path_node.revert_virtual_loss()
                path_node.visit_count += 1
                path_node.value_sum += value

                if path_node.visit_count >= 10 and path_node.q_value < -0.8:
                    path_node.is_pruned = True
                    logger.debug(f"Pruned branch {path_node.action_taken} with Q {path_node.q_value}")

    effective_threads = min(num_threads, engine.num_simulations)
    with ThreadPoolExecutor(max_workers=effective_threads) as executor:
        futures = [executor.submit(_single_simulation) for _ in range(engine.num_simulations)]
        for future in futures:
            try:
                future.result()
            except Exception as e:
                logger.warning(f"Parallel MCTS simulation failed: {e}")

    best_action = None
    max_visits = -1

    for action, child in root.children.items():
        if child.visit_count > max_visits:
            max_visits = child.visit_count
            best_action = action

    return best_action or legal_actions[0]
