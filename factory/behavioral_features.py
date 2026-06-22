import math
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class BehavioralVector:
    """
    Represents the playstyle and behavioral footprint of an agent during a game.
    Used for automated diversity mapping, anti-pattern extraction, and clustering.
    """
    turn_aggro: float          # Prize differential slope (0=passive, 1=all-out attack)
    energy_accel_rate: float   # Average energy attached per turn
    hand_disruption: float     # Fraction of trainer plays that disrupt opponent
    setup_duration: float      # Number of turns before first attack
    bench_density: float       # Average bench pokemon count across game
    evolution_depth: float     # Maximum evolution stage achieved (0-2)
    consistency: float         # 1 - stddev of hand_scores across turns

    def to_dict(self) -> dict:
        return {
            "turn_aggro": self.turn_aggro,
            "energy_accel_rate": self.energy_accel_rate,
            "hand_disruption": self.hand_disruption,
            "setup_duration": self.setup_duration,
            "bench_density": self.bench_density,
            "evolution_depth": self.evolution_depth,
            "consistency": self.consistency
        }

    def to_tensor(self) -> List[float]:
        return [
            self.turn_aggro, self.energy_accel_rate, self.hand_disruption,
            self.setup_duration, self.bench_density, self.evolution_depth,
            self.consistency
        ]

    def distance(self, other: 'BehavioralVector') -> float:
        """Euclidean distance between two behavioral vectors."""
        t1 = self.to_tensor()
        t2 = other.to_tensor()
        return math.sqrt(sum((a - b)**2 for a, b in zip(t1, t2)))

from factory.behavioral_feature_helpers import compute_from_steps, DiversityTracker
