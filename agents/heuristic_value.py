import random
import logging
from agents.value_network import BaseValueNetwork
from agents.card_registry import CardRegistry
from agents.heuristic_pipeline import _state_heuristics, _action_score

logger = logging.getLogger(__name__)

class HeuristicValueNetwork(BaseValueNetwork):
    def evaluate(self, game_state: dict, action: str = None, determinization: dict = None) -> float:
        if action is None:
            return 0.0
        if game_state.get("game_over"):
            return 1.0 if game_state.get("winner") == "me" else -1.0
        value = _state_heuristics(game_state)
        threat_penalty = 0.0
        if determinization and determinization.get("hand"):
            threat_penalty = len(determinization["hand"]) * 0.01
        value += _action_score(action, game_state, threat_penalty)
        value += random.uniform(-0.01, 0.01)
        return max(-1.0, min(1.0, value))
