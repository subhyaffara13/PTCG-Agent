from typing import Dict, Any
from dataclasses import dataclass, field

@dataclass
class BoardState:
    my_prizes_remaining: int = 6
    opponent_prizes_remaining: int = 6
    opponent_archetype_confidence: float = 0.0
    priority_profile: str = "aggro_push"
    turn_number: int = 1
    prized_probabilities: Dict[str, float] = field(default_factory=dict)
    my_bench_count: int = 0
    opponent_archetype: str = "unknown"
    bench_has_attacker: bool = False
    my_active_hp: int = 100

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BoardState":
        return cls(
            my_prizes_remaining=data.get("my_prizes_remaining", 6),
            opponent_prizes_remaining=data.get("opponent_prizes_remaining", 6),
            opponent_archetype_confidence=data.get("opponent_archetype_confidence", 0.0),
            priority_profile=data.get("priority_profile", "aggro_push"),
            turn_number=data.get("turn_number", 1),
            prized_probabilities=data.get("prized_probabilities", {}),
            my_bench_count=data.get("my_bench_count", 0),
            opponent_archetype=data.get("opponent_archetype", "unknown"),
            bench_has_attacker=data.get("bench_has_attacker", False),
            my_active_hp=data.get("my_active_hp", 100)
        )
