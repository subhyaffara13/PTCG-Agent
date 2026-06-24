import random
import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from dataclasses import dataclass

def __getattr__(name: str):
    if name == "HeuristicValueNetwork":
        from agents.heuristic_value import HeuristicValueNetwork
        return HeuristicValueNetwork
    raise AttributeError(f"module {__name__} has no attribute {name}")

logger = logging.getLogger(__name__)

@dataclass
class ActionPrior:
    action: str
    prob: float


class BaseValueNetwork(ABC):
    @abstractmethod
    def evaluate(self, game_state: dict, action: str = None, determinization: dict = None) -> float:
        pass

class NeuralValueNetwork(BaseValueNetwork):
    def __init__(self, weights_path="logs/model_weights.pth"):
        self.weights_path = Path(weights_path)
        self.heuristic, self.model = None, None
        from agents.value_network_helpers import PTCGValueMLP
        if PTCGValueMLP is not None and self.weights_path.exists():
            try:
                import torch
                self.model = PTCGValueMLP()
                self.model.load_state_dict(torch.load(str(self.weights_path), map_location="cpu"))
                self.model.eval()
            except: self.model = None
        if self.model is None:
            from agents.heuristic_value import HeuristicValueNetwork
            self.heuristic = HeuristicValueNetwork()

    def evaluate(self, game_state: dict, action: str = None, determinization: dict = None) -> float:
        if self.heuristic: return self.heuristic.evaluate(game_state, action, determinization)
        from agents.value_network_helpers import state_to_tensor
        try:
            import torch
            with torch.no_grad():
                val = self.model(state_to_tensor(game_state)).item()
                if action and action.startswith("attack:"): val += 0.2
                return max(-1.0, min(1.0, val))
        except:
            from agents.heuristic_value import HeuristicValueNetwork
            return HeuristicValueNetwork().evaluate(game_state, action, determinization)


class BasePolicyNetwork(ABC):
    @abstractmethod
    def get_priors(self, game_state: dict, legal_actions: List[str]) -> List[ActionPrior]:
        pass

class HeuristicPolicyNetwork(BasePolicyNetwork):

    def get_priors(self, game_state: dict, legal_actions: List[str]) -> List[ActionPrior]:
        priors = []
        if not legal_actions:
            return priors

        base_prob = 1.0 / len(legal_actions)
        for action in legal_actions:
            prob = base_prob
            if action.startswith("attack:"):
                prob *= 2.0
            elif action.startswith("evolve:"):
                prob *= 1.5
            elif action.startswith("attach_energy:"):
                prob *= 1.3
            elif action.startswith("retreat:"):
                prob *= 1.2

            priors.append(ActionPrior(action=action, prob=prob))

        # Normalize
        total = sum(p.prob for p in priors)
        if total > 0:
            for p in priors:
                p.prob /= total

        return priors
