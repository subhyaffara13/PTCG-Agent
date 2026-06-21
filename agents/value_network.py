"""
agents/value_network.py

Defines abstract interfaces for Value and Policy networks used by the MCTS engine.
Provides heuristic implementations that replicate the existing hand-tuned evaluation
logic, allowing seamless replacement with learned neural networks in the future.
"""

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
    """An action paired with its prior probability from the policy network."""
    action: str
    prob: float


class BaseValueNetwork(ABC):
    """
    Abstract base class for value estimation.
    """

    @abstractmethod
    def evaluate(self, game_state: dict, action: str = None, determinization: dict = None) -> float:
        """
        Evaluate the desirability of a state (optionally after taking an action).
        """
        ...


class BasePolicyNetwork(ABC):
    """
    Abstract base class for action prior generation.
    """

    @abstractmethod
    def get_priors(self, game_state: dict, legal_actions: List[str]) -> List[ActionPrior]:
        """
        Generate prior probabilities for each legal action.
        """
        ...


class HeuristicPolicyNetwork(BasePolicyNetwork):
    """
    Hand-tuned heuristic policy network extracted from the original MCTSEngine._get_action_priors.
    """

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
