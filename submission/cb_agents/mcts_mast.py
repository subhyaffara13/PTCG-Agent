import random
from collections import defaultdict
from typing import Dict, List

class MASTPolicy:
    """Tracks action -> win statistics across all MCTS rollouts."""
    
    def __init__(self, exploration_weight: float = 0.3):
        self.action_wins: Dict[str, int] = defaultdict(int)
        self.action_visits: Dict[str, int] = defaultdict(int)
        self.exploration_weight = exploration_weight
    
    def update(self, actions_played: List[str], won: bool):
        """Update statistics after a rollout completes."""
        for action in actions_played:
            self.action_visits[action] += 1
            if won:
                self.action_wins[action] += 1
    
    def get_action_prior(self, action: str) -> float:
        """Blend MAST statistics with default policy prior."""
        if self.action_visits[action] == 0:
            return 0.5
        return self.action_wins[action] / self.action_visits[action]
    
    def select_rollout_action(self, legal_actions: List[str]) -> str:
        """ε-greedy: exploration_weight chance of random, else pick highest win-rate."""
        if not legal_actions:
            return None
        if random.random() < self.exploration_weight:
            return random.choice(legal_actions)
            
        best_action = None
        best_rate = -1.0
        
        for action in legal_actions:
            if self.action_visits[action] == 0:
                # optimistic prior for unvisited actions
                rate = 1.0 
            else:
                rate = self.action_wins[action] / self.action_visits[action]
                
            if rate > best_rate:
                best_rate = rate
                best_action = action
                
        return best_action if best_action is not None else random.choice(legal_actions)
