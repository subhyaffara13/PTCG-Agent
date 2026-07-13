import random, logging
from abc import ABC, abstractmethod
from typing import List, Any
from dataclasses import dataclass
from pathlib import Path
import os

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
    def evaluate(self, game_state: dict, action: str | None = None, determinization: dict | None = None) -> float:
        pass

class NeuralValueNetwork(BaseValueNetwork):
    heuristic: Any
    model: Any

    def __init__(self, model_path: str = "logs/model_weights.pth", device: str = "cpu"):
        from cb_agents.value_network_helpers import ActorCritic, state_to_tensor, state_to_card_tokens, HAS_TORCH
        from factory.state_dimensions import STATE_DIM

        self.device = device
        self.model = None
        self.state_to_tensor = state_to_tensor
        self.state_to_card_tokens = state_to_card_tokens
        self.has_torch = HAS_TORCH

        if HAS_TORCH:
            try:
                import torch
                tnet = ActorCritic(input_dim=STATE_DIM, hidden_dim=128, action_dim=3000)
                tnet.to(self.device)
                
                if os.path.exists(model_path):
                    state_dict = torch.load(model_path, map_location=self.device, weights_only=True)
                    model_keys = set(state_dict.keys())
                    if any("encoder" in k or "actor" in k for k in model_keys):
                        tnet.load_state_dict(state_dict, strict=False)
                        self.model = tnet
                        self.model.eval()
                        logger.info(f"Loaded ActorCritic from {model_path} successfully.")
                    else:
                        logger.warning("Checkpoint keys do not match ActorCritic. Falling back to HeuristicValueNetwork.")
                else:
                    logger.warning(f"No checkpoint found at {model_path}. Using untutored ActorCritic.")
                    self.model = tnet
                    self.model.eval()
            except Exception as e:
                logger.warning(f"ActorCritic load failed: {e}. Falling back to HeuristicValueNetwork.")
                self.model = None

    def evaluate(self, game_state: dict, action: str | None = None, determinization: dict | None = None) -> float:
        if game_state.get("game_over"):
            return 1.0 if game_state.get("winner") == "me" else -1.0
            
        if self.model is None or not self.has_torch:
            from cb_agents.heuristic_value import HeuristicValueNetwork
            return HeuristicValueNetwork().evaluate(game_state, action, determinization)
            
        import torch
        with torch.no_grad():
            try:
                t, z, s, m = self.state_to_card_tokens(game_state)
                if t is not None:
                    t = t.to(self.device)
                    z = z.to(self.device)
                    s = s.to(self.device)
                    m = m.to(self.device)
                    logits, value = self.model(x=None, token_ids=t, zone_ids=z, scalars=s, padding_mask=m)
                    val = value.item()
                else:
                    legacy_tensor = self.state_to_tensor(game_state)
                    if legacy_tensor is not None:
                        legacy_tensor = legacy_tensor.to(self.device)
                        logits, value = self.model(x=legacy_tensor)
                        val = value.item()
                    else:
                        val = 0.0
                        
                if action:
                    from cb_agents.heuristic_pipeline import _action_score
                    val += _action_score(action, game_state, 0.0)
                return max(-1.0, min(1.0, val))
            except Exception as e:
                logger.error(f"Neural evaluation failed: {e}")
                
        from cb_agents.heuristic_value import HeuristicValueNetwork
        return HeuristicValueNetwork().evaluate(game_state, action, determinization)
        
    def get_action_priors(self, game_state: dict, candidates: list) -> dict:
        if self.model is None or not self.has_torch or not candidates:
            return {}
            
        import torch
        from factory.data_alignment_helpers import normalize_action
        with torch.no_grad():
            try:
                t, z, s, m = self.state_to_card_tokens(game_state)
                if t is not None:
                    t = t.to(self.device)
                    z = z.to(self.device)
                    s = s.to(self.device)
                    m = m.to(self.device)
                    logits, value = self.model(x=None, token_ids=t, zone_ids=z, scalars=s, padding_mask=m)
                else:
                    legacy_tensor = self.state_to_tensor(game_state)
                    if legacy_tensor is not None:
                        legacy_tensor = legacy_tensor.to(self.device)
                        logits, value = self.model(x=legacy_tensor)
                    else:
                        return {}
                        
                probs = torch.softmax(logits.squeeze(0), dim=-1).cpu().numpy()
                
                priors = {}
                for action_str in candidates:
                    action_id = normalize_action(action_str, offset_play=0, offset_attack=1000, offset_other=2000)
                    if 0 <= action_id < len(probs):
                        priors[action_str] = float(probs[action_id])
                    else:
                        priors[action_str] = 0.0
                        
                return priors
                
            except Exception as e:
                logger.error(f"Neural action prior extraction failed: {e}")
                return {}

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


class PPOPolicyNetwork(BasePolicyNetwork):
    def __init__(self, model_path="models/ppo_actor_critic.pt", device="cpu"):
        self.model = None
        self.device = device
        self._state_to_tensor = None
        self._state_to_card_tokens = None
        self._has_torch = False
        self._heuristic_fallback = HeuristicPolicyNetwork()

        try:
            import torch as _
        except ImportError:
            logger.info("PyTorch not available. PPOPolicyNetwork will use heuristic fallback.")
            return

        from cb_agents.value_network_helpers import state_to_tensor, state_to_card_tokens, HAS_TORCH
        from factory.ppo_trainer_network import ActorCritic
        from factory.state_dimensions import STATE_DIM

        self._has_torch = HAS_TORCH
        self._state_to_tensor = state_to_tensor
        self._state_to_card_tokens = state_to_card_tokens

        if not HAS_TORCH:
            logger.info("Torch helpers unavailable. PPOPolicyNetwork using heuristic fallback.")
            return

        if not os.path.exists(model_path):
            logger.info(f"PPO model not found at {model_path}. Using heuristic policy fallback.")
            return

        try:
            import torch
            ac = ActorCritic(input_dim=STATE_DIM, hidden_dim=128, action_dim=3000)
            ac.load_state_dict(torch.load(model_path, map_location=self.device, weights_only=True))
            ac.to(self.device)
            ac.eval()
            self.model = ac
            logger.info(f"Loaded PPO policy network from {model_path}")
        except Exception as e:
            logger.warning(f"PPO policy load failed: {e}. Using heuristic fallback.")

    def get_priors(self, game_state: dict, legal_actions: List[str]) -> List[ActionPrior]:
        if self.model is None or not self._has_torch or not legal_actions:
            return self._heuristic_fallback.get_priors(game_state, legal_actions)

        import torch
        from factory.data_alignment_helpers import normalize_action

        with torch.no_grad():
            try:
                t, z, s, m = self._state_to_card_tokens(game_state)
                if t is not None:
                    t = t.to(self.device)
                    z = z.to(self.device)
                    s = s.to(self.device)
                    m = m.to(self.device)
                    logits, _ = self.model(x=None, token_ids=t, zone_ids=z, scalars=s, padding_mask=m)
                else:
                    tensor = self._state_to_tensor(game_state)
                    if tensor is not None:
                        tensor = tensor.to(self.device)
                        logits, _ = self.model(x=tensor)
                    else:
                        return self._heuristic_fallback.get_priors(game_state, legal_actions)

                probs = torch.softmax(logits.squeeze(0), dim=-1).cpu().numpy()

                priors = []
                for action_str in legal_actions:
                    action_id = normalize_action(action_str, offset_play=0, offset_attack=1000, offset_other=2000)
                    prob = float(probs[action_id]) if 0 <= action_id < len(probs) else 0.0
                    priors.append(ActionPrior(action=action_str, prob=prob))

                total = sum(p.prob for p in priors)
                if total > 0:
                    for p in priors:
                        p.prob /= total
                return priors

            except Exception as e:
                logger.error(f"PPO policy inference failed: {e}")
                return self._heuristic_fallback.get_priors(game_state, legal_actions)


class PPOValueNetwork(BaseValueNetwork):
    def __init__(self, model_path="models/ppo_actor_critic.pt", device="cpu"):
        self.model = None
        self.device = device
        self._state_to_tensor = None
        self._state_to_card_tokens = None
        self._has_torch = False

        try:
            import torch as _
        except ImportError:
            logger.info("PyTorch not available. PPOValueNetwork will use heuristic fallback.")
            return

        from cb_agents.value_network_helpers import state_to_tensor, state_to_card_tokens, HAS_TORCH
        from factory.ppo_trainer_network import ActorCritic
        from factory.state_dimensions import STATE_DIM

        self._has_torch = HAS_TORCH
        self._state_to_tensor = state_to_tensor
        self._state_to_card_tokens = state_to_card_tokens

        if not HAS_TORCH:
            logger.info("Torch helpers unavailable. PPOValueNetwork using heuristic fallback.")
            return

        if not os.path.exists(model_path):
            logger.info(f"PPO model not found at {model_path}. Using heuristic value fallback.")
            return

        try:
            import torch
            ac = ActorCritic(input_dim=STATE_DIM, hidden_dim=128, action_dim=3000)
            ac.load_state_dict(torch.load(model_path, map_location=self.device, weights_only=True))
            ac.to(self.device)
            ac.eval()
            self.model = ac
            logger.info(f"Loaded PPO value network from {model_path}")
        except Exception as e:
            logger.warning(f"PPO value load failed: {e}. Using heuristic fallback.")

    def evaluate(self, game_state: dict, action: str | None = None, determinization: dict | None = None) -> float:
        if game_state.get("game_over"):
            return 1.0 if game_state.get("winner") == "me" else -1.0

        if self.model is None or not self._has_torch:
            return HeuristicValueNetwork().evaluate(game_state, action, determinization)

        import torch
        with torch.no_grad():
            try:
                t, z, s, m = self._state_to_card_tokens(game_state)
                if t is not None:
                    t = t.to(self.device)
                    z = z.to(self.device)
                    s = s.to(self.device)
                    m = m.to(self.device)
                    _, val = self.model(x=None, token_ids=t, zone_ids=z, scalars=s, padding_mask=m)
                else:
                    tensor = self._state_to_tensor(game_state)
                    if tensor is not None:
                        tensor = tensor.to(self.device)
                        _, val = self.model(x=tensor)
                    else:
                        return HeuristicValueNetwork().evaluate(game_state, action, determinization)

                v = val.item()
                if action:
                    from cb_agents.heuristic_pipeline import _action_score
                    v += _action_score(action, game_state, 0.0)
                return max(-1.0, min(1.0, v))

            except Exception as e:
                logger.error(f"PPO value inference failed: {e}")
                return HeuristicValueNetwork().evaluate(game_state, action, determinization)
