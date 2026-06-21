import logging
from typing import List

from agents.value_network import (
    BaseValueNetwork, BasePolicyNetwork,
    HeuristicValueNetwork, HeuristicPolicyNetwork,
    ActionPrior,
)
from agents.action_masker import ActionMasker
from agents.mcts_node import MCTSNode
from agents.mcts_parallel import run_parallel_search
from agents.mcts_selection import select_child

logger = logging.getLogger(__name__)

# Re-export ActionPrior and MCTSNode for backward compatibility
__all__ = ['ActionPrior', 'MCTSNode', 'MCTSEngine']


class MCTSEngine:
    """
    Monte Carlo Tree Search (AlphaZero style) for Pokémon TCG.
    """
    def __init__(self, c_puct: float = 1.25, num_simulations: int = 50, belief_tracker=None,
                 value_network: BaseValueNetwork = None, policy_network: BasePolicyNetwork = None,
                 action_masker: ActionMasker = None):
        self.c_puct = c_puct
        self.num_simulations = num_simulations
        self.belief_tracker = belief_tracker
        self.value_network = value_network or HeuristicValueNetwork()
        self.policy_network = policy_network or HeuristicPolicyNetwork()
        self.action_masker = action_masker or ActionMasker()

    def _get_action_priors(self, game_state: dict, legal_actions: List[str]) -> List[ActionPrior]:
        return self.policy_network.get_priors(game_state, legal_actions)

    def _evaluate_state(self, game_state: dict, action: str, determinization: dict = None) -> float:
        return self.value_network.evaluate(game_state, action, determinization)

    def search(self, game_state: dict, legal_actions: List[str]) -> str:
        """Executes MCTS from the current state and returns the best action."""
        if not legal_actions:
            return "pass"
        if len(legal_actions) == 1:
            return legal_actions[0]

        canonical_actions, groups_map = self.action_masker.get_canonical_actions(
            legal_actions, game_state
        )
        if len(canonical_actions) == 1:
            return canonical_actions[0]

        root_hash = f"turn_{game_state.get('turn_number', 0)}"
        root = MCTSNode(state_hash=root_hash)
        priors = self._get_action_priors(game_state, canonical_actions)
        root.expand(priors)

        for _ in range(self.num_simulations):
            node = root
            search_path = [node]
            determinization = None
            if self.belief_tracker:
                determinization = self.belief_tracker.sample_determinization()
            while node.is_expanded():
                node = select_child(node, self.c_puct)
                search_path.append(node)
            value = self._evaluate_state(game_state, node.action_taken, determinization)
            for path_node in reversed(search_path):
                path_node.visit_count += 1
                path_node.value_sum += value
                if path_node.visit_count >= 10 and path_node.q_value < -0.8:
                    path_node.is_pruned = True
                    logger.debug(f"Pruned branch {path_node.action_taken} with Q {path_node.q_value}")

        best_action = None
        max_visits = -1
        for action, child in root.children.items():
            if child.visit_count > max_visits:
                max_visits = child.visit_count
                best_action = action
        return best_action or legal_actions[0]

    def parallel_search(self, game_state: dict, legal_actions: List[str],
                        num_threads: int = 4) -> str:
        """Executes MCTS with virtual loss using multiple threads."""
        return run_parallel_search(self, game_state, legal_actions, num_threads)
