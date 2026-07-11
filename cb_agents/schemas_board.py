from typing import Any, Dict
from dataclasses import dataclass, field

@dataclass
class BoardSummary:
    my_prizes_remaining: int = 6
    opponent_prizes_remaining: int = 6
    my_active_hp: int = 100
    opponent_active_hp: int = 100
    turn_number: int = 1
    opponent_archetype: str = "unknown"
    opponent_archetype_confidence: float = 0.0
    bench_has_attacker: bool = False
    my_bench_count: int = 0
    my_deck_count: int = 60
    opponent_deck_count: int = 60
    prized_probabilities: Dict[str, float] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "BoardSummary":
        return cls(
            my_prizes_remaining=d.get("my_prizes_remaining", 6),
            opponent_prizes_remaining=d.get("opponent_prizes_remaining", 6),
            my_active_hp=d.get("my_active_hp", 100),
            opponent_active_hp=d.get("opponent_active_hp", 100),
            turn_number=d.get("turn_number", 1),
            opponent_archetype=d.get("opponent_archetype", "unknown"),
            opponent_archetype_confidence=d.get("opponent_archetype_confidence", 0.0),
            bench_has_attacker=d.get("bench_has_attacker", False),
            my_bench_count=d.get("my_bench_count", 0),
            my_deck_count=d.get("my_deck_count", 60),
            opponent_deck_count=d.get("opponent_deck_count", 60),
            prized_probabilities=d.get("prized_probabilities", {}),
        )
