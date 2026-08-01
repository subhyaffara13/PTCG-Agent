from . import ABC, abstractmethod, dataclass

from utils.__getattr__ import __getattr__

@dataclass
class ActionPrior:
    action: str
    prob: float

class BaseValueNetwork(ABC):
    @abstractmethod
    def evaluate(self, game_state: dict, action: str | None = None, determinization: dict | None = None) -> float:
        pass

