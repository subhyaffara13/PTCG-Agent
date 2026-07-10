import time
import logging
from typing import List
from cb_agents.mcts_node import MCTSNode
from cb_agents.forward_model import apply_action
from cb_agents.heuristic_pipeline import pipeline
from cb_agents.value_network import ActionPrior

logger = logging.getLogger(__name__)

def run_mcts_simulations(engine, root: MCTSNode, game_state: dict, canonical_actions: List[str], mast_policy, time_remaining: float | None):
    # Cap max time for Python MCTS fallback to 0.15s to prevent 20-minute stalls on worker nodes
    max_time = 0.15
    if time_remaining is not None:
        max_time = max(0.01, min(max_time, time_remaining - 0.5))
        
    start_time = time.time()
    for _ in range(engine.num_simulations):
        elapsed = time.time() - start_time
        if time_remaining is not None and time_remaining - elapsed < 0.5:
            logger.debug(f"MCTS early abort: critical time ({_} sims, {elapsed:.2f}s)")
            break
        if elapsed > max_time:
            logger.debug(f"MCTS early after {_} sims ({elapsed:.2f}s)")
            break
        det = engine.belief_tracker.sample_determinization() if engine.belief_tracker else None

        path = [root]
        node = engine.select_child(root, engine.c_puct)
        if node is None: continue
        path.append(node)
        current_gs = game_state
        depth = 0
        while node.is_expanded() and depth < 50:
            depth += 1
            if getattr(node, "is_terminal", False):
                break
            current_gs = apply_action(current_gs, node.action_taken)
            next_node = engine._sample_chance_child(node) if node.is_chance_node else engine.select_child(node, engine.c_puct)
            if next_node is None: break
            node = next_node
            path.append(node)
        if node is None: continue

        next_gs = apply_action(current_gs, node.action_taken)
        val = engine._evaluate_state(next_gs, node.action_taken, det)
        
        if next_gs.get("turn_ended") == True or next_gs.get("game_over") == True:
            node.is_terminal = True
        else:
            next_legal_actions = next_gs.get("legal_actions", [])
            if not next_legal_actions: next_legal_actions = ["pass"]
            try:
                canonical_next, _ = pipeline.mask_actions(next_legal_actions, next_gs)
            except Exception as e:
                logger.error(f"mask_actions failed: {e}")
                canonical_next = next_legal_actions
            if not canonical_next:
                canonical_next = ["pass"]
            new_priors = engine._get_action_priors(next_gs, canonical_next, mast_policy)
            if not new_priors and canonical_next == ["pass"]:
                new_priors = [ActionPrior(action="pass", prob=1.0)]
            if new_priors:
                node.expand(new_priors)

        current_val = val
        for n in reversed(path):
            n.visit_count += 1
            n.value_sum += current_val
        
        actions_played = [n.action_taken for n in path if getattr(n, "action_taken", None) is not None]
        mast_policy.update(actions_played, won=(val > 0))
