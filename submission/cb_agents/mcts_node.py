import threading
from typing import Dict, List, Any
from cb_agents.value_network import ActionPrior

class MCTSNode:
    def __init__(self, state_hash: str, parent=None, action_taken: str = None, prior_prob: float = 1.0, is_chance_node: bool = False):
        self.state_hash = state_hash
        self.parent = parent
        self.action_taken = action_taken
        self.children: Dict[str, 'MCTSNode'] = {}
        self.visit_count = 0
        self.value_sum = 0.0
        self.prior_prob = prior_prob
        self.is_chance_node = is_chance_node
        self.is_pruned = False
        self.virtual_loss = 0.0
        self._lock = threading.Lock()

    @property
    def q_value(self) -> float:
        if self.visit_count == 0: return 0.0
        return (self.value_sum + self.virtual_loss) / self.visit_count

    @property
    def real_q_value(self) -> float:
        if self.visit_count == 0: return 0.0
        return self.value_sum / self.visit_count

    def apply_virtual_loss(self, loss: float = -1.0):
        with self._lock:
            self.virtual_loss += loss
            self.visit_count += 1

    def revert_virtual_loss(self, loss: float = -1.0):
        with self._lock:
            self.virtual_loss -= loss
            self.visit_count -= 1

    def expand(self, action_priors: List[ActionPrior]):
        chance_actions = ["crushing_hammer", "pokemon_catcher", "super_scoop_up", "pokeball"]
        for ap in action_priors:
            if ap.action not in self.children:
                is_chance = any(ca in ap.action.lower() for ca in chance_actions)
                if is_chance:
                    chance_node = MCTSNode(
                        state_hash=f"{self.state_hash}_{ap.action}_chance",
                        parent=self, action_taken=ap.action, prior_prob=ap.prob, is_chance_node=True)
                    chance_node.children["heads"] = MCTSNode(
                        state_hash=f"{self.state_hash}_{ap.action}_heads",
                        parent=chance_node, action_taken=f"{ap.action}_heads", prior_prob=0.5)
                    chance_node.children["tails"] = MCTSNode(
                        state_hash=f"{self.state_hash}_{ap.action}_tails",
                        parent=chance_node, action_taken=f"{ap.action}_tails", prior_prob=0.5)
                    self.children[ap.action] = chance_node
                else:
                    self.children[ap.action] = MCTSNode(
                        state_hash=f"{self.state_hash}_{ap.action}",
                        parent=self, action_taken=ap.action, prior_prob=ap.prob)

    def is_expanded(self) -> bool:
        return len(self.children) > 0
