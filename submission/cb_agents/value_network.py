import random, logging
from abc import ABC, abstractmethod
from typing import List
from dataclasses import dataclass
from pathlib import Path

def __getattr__(name):
    if name == "HeuristicValueNetwork":
        from cb_agents.heuristic_value import HeuristicValueNetwork
        return HeuristicValueNetwork
    raise AttributeError(f"module {__name__} no attr {name}")

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
        self.heuristic, self.model, self._state_cache = None, None, {}
        from cb_agents.value_network_helpers import PTCGValueMLP
        if PTCGValueMLP is not None and self.weights_path.exists():
            try:
                import torch
                self.model = PTCGValueMLP()
                self.model.load_state_dict(torch.load(str(self.weights_path), map_location="cpu"))
                self.model.eval()
            except: self.model = None
        if self.model is None:
            from cb_agents.heuristic_value import HeuristicValueNetwork
            self.heuristic = HeuristicValueNetwork()

    def evaluate(self, gs: dict, action: str = None, det: dict = None) -> float:
        if gs.get("game_over"):
            return 1.0 if gs.get("winner") == "me" else -1.0
        if self.heuristic: return self.heuristic.evaluate(gs, action, det)
        from cb_agents.value_network_helpers import state_to_tensor
        from cb_agents.heuristic_pipeline import _action_score
        try:
            import torch
            hand_sorted = sorted([str(x) for x in gs.get("my_hand", [])]) if isinstance(gs.get("my_hand"), list) else []
            active = gs.get("my_active_pokemon", {})
            active_id = str(active.get("id")) if isinstance(active, dict) else None
            active_attached_sorted = sorted([str(x) for x in active.get("attached", [])]) if isinstance(active, dict) else []
            bench_strs = sorted([str(x) for x in gs.get("my_bench", [])]) if isinstance(gs.get("my_bench"), list) else []
            h = hash((str(hand_sorted),
                      str(gs.get("turn_number", 0)),
                      str(active_id),
                      str(active_attached_sorted),
                      str(bench_strs),
                      gs.get("my_active_damage", 0),
                      gs.get("my_prizes", 6),
                      gs.get("opponent_prizes", 6),
                      gs.get("opponent_active_hp", 100)))
            if h not in self._state_cache:
                with torch.no_grad():
                    self._state_cache[h] = self.model(state_to_tensor(gs)).item()
            val = self._state_cache[h]
            if action: val += _action_score(action, gs, 0.0)
            return max(-1.0, min(1.0, val))
        except:
            from cb_agents.heuristic_value import HeuristicValueNetwork
            return HeuristicValueNetwork().evaluate(gs, action, det)

class BasePolicyNetwork(ABC):
    @abstractmethod
    def get_priors(self, game_state: dict, legal_actions: List[str]) -> List:
        pass

class HeuristicPolicyNetwork(BasePolicyNetwork):
    def get_priors(self, gs: dict, legal_actions: List[str]) -> List[ActionPrior]:
        priors = []
        if not legal_actions: return priors
        pid = gs.get("prized_card_ids", {})
        pc = gs.get("prize_certainty", 0.0)
        bp = 1.0 / len(legal_actions)
        for a in legal_actions:
            p = bp
            if a.startswith("attack:"): p *= 2.0
            elif a.startswith("evolve:"): p *= 1.5
            elif a.startswith("attach_energy:"): p *= 1.3
            elif a.startswith("ability:"): p *= 1.5
            elif a.startswith("retreat:"): p *= 1.2
            elif a.startswith("play_trainer:"):
                if pc > 0 and sum(pid.values()) <= 2: p *= 1.3
            priors.append(ActionPrior(action=a, prob=p))
        total = sum(pr.prob for pr in priors)
        if total > 0:
            for pr in priors: pr.prob /= total
        return priors
