import math
import random
import logging
from cb_agents.mcts_node import MCTSNode

logger = logging.getLogger(__name__)

class MCTSSelectionMixin:
    def calculate_ucb(self, node: MCTSNode, total_parent_visits: int, c_puct: float) -> float:
        """Calculates the PUCT (Predictor Upper Confidence bound for Trees) score."""
        q_value = node.q_value
        u_value = c_puct * node.prior_prob * math.sqrt(total_parent_visits) / (1 + node.visit_count)
        return q_value + u_value

    def select_child(self, node: MCTSNode, c_puct: float) -> MCTSNode:
        """Selects the child with the highest UCB score, or samples probabilistically for chance nodes."""
        if node.is_chance_node:
            return self._sample_chance_child(node)

        best_score = -float('inf')
        best_child = None
        for child in node.children.values():
            if child.is_pruned:
                continue
            score = self.calculate_ucb(child, node.visit_count, c_puct)
            if score > best_score:
                best_score = score
                best_child = child

        if not best_child and node.children:
            best_child = list(node.children.values())[0]

        return best_child

    def _sample_chance_child(self, node: MCTSNode) -> MCTSNode:
        """Sample a child from a chance node proportional to prior probabilities."""
        r = random.random()
        cumulative = 0.0
        for child in node.children.values():
            cumulative += child.prior_prob
            if r <= cumulative:
                return child
        return list(node.children.values())[-1]
