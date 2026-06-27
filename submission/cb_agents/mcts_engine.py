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

logger = logging.getLogger(__name__)

class MCTSEngine(MCTSSelectionMixin, MCTSParallelMixin):
    def __init__(self, c_puct: float = 1.25, num_simulations: int = 50, belief_tracker=None,
                 value_network: BaseValueNetwork = None, policy_network: BasePolicyNetwork = None):
        self.c_puct = c_puct
        self.num_simulations = num_simulations
        self.belief_tracker = belief_tracker
        self.value_network = value_network or HeuristicValueNetwork()
        self.policy_network = policy_network or HeuristicPolicyNetwork()

    def _get_action_priors(self, game_state: dict, legal_actions: List[str]) -> List[ActionPrior]:
        return self.policy_network.get_priors(game_state, legal_actions)

    def _evaluate_state(self, game_state: dict, action: str, determinization: dict = None) -> float:
        return self.value_network.evaluate(game_state, action, determinization)

    def search(self, game_state: dict, legal_actions: List[str], time_remaining: float = None) -> str:
        if not legal_actions:
            return "pass"
        import os
        if os.environ.get("FAST_SIM_MODE") == "true":
            return legal_actions[0]
        if len(legal_actions) == 1:
            return legal_actions[0]

        canonical_actions, groups_map = pipeline.mask_actions(legal_actions, game_state)
        if len(canonical_actions) == 1:
            return canonical_actions[0]

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
        priors = self._get_action_priors(game_state, canonical_actions)
        root.expand(priors)

        import time
        max_time = max(1.0, self.num_simulations * 0.2)
        if time_remaining is not None:
            max_time = min(max_time, time_remaining - 0.5)
            
        start_time = time.time()
        for _ in range(self.num_simulations):
            elapsed = time.time() - start_time
            if time_remaining is not None and time_remaining - elapsed < 0.5:
                logger.debug(f"MCTS early abort: critical time ({_} sims, {elapsed:.2f}s)")
                break
            if _ % 10 == 0 and elapsed > max_time:
                logger.debug(f"MCTS early after {_} sims ({elapsed:.2f}s)")
                break
            det = self.belief_tracker.sample_determinization() if self.belief_tracker else None

            path = [root]
            node = self.select_child(root, self.c_puct)
            if node is None: continue
            path.append(node)
            current_gs = game_state
            while node.is_expanded():
                current_gs = apply_action(current_gs, node.action_taken)
                node = self._sample_chance_child(node) if node.is_chance_node else self.select_child(node, self.c_puct)
                if node is None: break
                path.append(node)
            if node is None: continue

            next_gs = apply_action(current_gs, node.action_taken)
            val = self._evaluate_state(next_gs, node.action_taken, det)
            
            if next_gs.get("turn_ended") == True or next_gs.get("game_over") == True:
                pass
            else:
                next_legal_actions = next_gs.get("legal_actions", [])
                if not next_legal_actions: next_legal_actions = ["pass"]
                canonical_next, _ = pipeline.mask_actions(next_legal_actions, next_gs)
                if not canonical_next:
                    canonical_next = ["pass"]
                new_priors = self.policy_network.get_priors(next_gs, canonical_next)
                if not new_priors and canonical_next == ["pass"]:
                    new_priors = [ActionPrior(action="pass", prob=1.0)]
                if new_priors:
                    node.expand(new_priors)

            current_val = val
            for n in reversed(path):
                n.visit_count += 1
                n.value_sum += current_val

        best_action, mv = None, -1
        for act, child in root.children.items():
            if child.visit_count > mv:
                mv, best_action = child.visit_count, act
        return best_action or legal_actions[0]
