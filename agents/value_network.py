import random, logging
from abc import ABC, abstractmethod
from typing import List, Any
from dataclasses import dataclass
from pathlib import Path
import os

is_kaggle = any(k.startswith("KAGGLE") for k in os.environ) or not os.path.exists("build_submission.py")

if is_kaggle:
    class MockNoGrad:
        def __enter__(self): return self
        def __exit__(self, *args): pass
    class MockTorch:
        no_grad = MockNoGrad
    torch = MockTorch()
else:
    try:
        import torch
    except ImportError:
        class MockNoGrad:
            def __enter__(self): return self
            def __exit__(self, *args): pass
        class MockTorch:
            no_grad = MockNoGrad
        torch = MockTorch()

def __getattr__(name):
    if name == "HeuristicValueNetwork":
        from agents.heuristic_value import HeuristicValueNetwork
        return HeuristicValueNetwork
    raise AttributeError(f"module {__name__} no attr {name}")

logger = logging.getLogger(__name__)

@dataclass
class ActionPrior:
    action: str
    prob: float

class BaseValueNetwork(ABC):
    @abstractmethod
    def evaluate(self, game_state: dict, action: str | None = None, determinization: dict | None = None) -> float:
        pass

class NeuralValueNetwork(BaseValueNetwork):
    heuristic: Any
    model: Any

    def __init__(self, weights_path="logs/model_weights.pth"):
        agent_dir = Path(__file__).parent.parent.resolve()
        self.weights_path = agent_dir / weights_path
        self.heuristic = None
        self.model = None
        self._state_cache = {}
        from agents.value_network_helpers import PTCGValueMLP, load_weights
        if PTCGValueMLP is not None and self.weights_path.exists():
            try:
                self.model = PTCGValueMLP()
                state_dict = load_weights(self.weights_path)
                self.model.load_state_dict(state_dict)
                self.model.eval()
            except Exception as e:
                logger.error(f"Failed to load neural value network: {e}")
                self.model = None
        if self.model is None:
            from agents.heuristic_value import HeuristicValueNetwork
            self.heuristic = HeuristicValueNetwork()

    def evaluate(self, game_state: dict, action: str | None = None, determinization: dict | None = None) -> float:
        if game_state.get("game_over"):
            return 1.0 if game_state.get("winner") == "me" else -1.0
        if self.heuristic: return self.heuristic.evaluate(game_state, action, determinization)
        from agents.value_network_helpers import state_to_tensor
        from agents.heuristic_pipeline import _action_score
        try:
            hand_sorted = sorted([str(x) for x in game_state.get("my_hand", [])]) if isinstance(game_state.get("my_hand"), list) else []
            active = game_state.get("my_active_pokemon", {})
            active_id = str(active.get("id")) if isinstance(active, dict) else None
            active_attached_sorted = sorted([str(x) for x in active.get("attached", [])]) if isinstance(active, dict) else []
            bench_strs = sorted([str(x) for x in game_state.get("my_bench", [])]) if isinstance(game_state.get("my_bench"), list) else []
            opp_bench_strs = sorted([str(x) for x in game_state.get("opponent_bench", [])]) if isinstance(game_state.get("opponent_bench"), list) else []
            my_discard_size = len(game_state.get("my_discard_pile", [])) if isinstance(game_state.get("my_discard_pile"), list) else 0
            opp_discard_size = len(game_state.get("opponent_discard_pile", [])) if isinstance(game_state.get("opponent_discard_pile"), list) else 0
            stadium = game_state.get("stadium_card")
            
            h = hash((str(hand_sorted),
                      str(game_state.get("turn_number", 0)),
                      str(active_id),
                      str(active_attached_sorted),
                      str(bench_strs),
                      str(opp_bench_strs),
                      str(my_discard_size),
                      str(opp_discard_size),
                      str(stadium),
                      game_state.get("my_active_damage", 0),
                      game_state.get("my_prizes", 6),
                      game_state.get("opponent_prizes", 6),
                      game_state.get("opponent_active_hp", 100)))
            val = 0.0
            if self.model is not None and state_to_tensor is not None:
                if h not in self._state_cache:
                    with torch.no_grad():
                        self._state_cache[h] = self.model(state_to_tensor(game_state)).item()
                val = self._state_cache[h]
            if action: val += _action_score(action, game_state, 0.0)
            return max(-1.0, min(1.0, val))
        except:
            from agents.heuristic_value import HeuristicValueNetwork
            return HeuristicValueNetwork().evaluate(game_state, action, determinization)

class BasePolicyNetwork(ABC):
    @abstractmethod
    def get_priors(self, game_state: dict, legal_actions: List[str]) -> List:
        pass

class HeuristicPolicyNetwork(BasePolicyNetwork):
    def get_priors(self, game_state: dict, legal_actions: List[str]) -> List[ActionPrior]:
        priors = []
        if not legal_actions: return priors
        pid = game_state.get("prized_card_ids", {})
        pc = game_state.get("prize_certainty", 0.0)
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
