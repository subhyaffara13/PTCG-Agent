from typing import Any, Dict, List
from dataclasses import dataclass, field

@dataclass
class PlayerObservation:
    hand: List[int] = field(default_factory=list)
    active: List[Any] = field(default_factory=list)
    bench: List[Any] = field(default_factory=list)
    prize: List[Any] = field(default_factory=list)
    discard: List[Any] = field(default_factory=list)
    deckCount: int = 60

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "PlayerObservation":
        return cls(
            hand=d.get("hand", []),
            active=d.get("active", []),
            bench=d.get("bench", []),
            prize=d.get("prize", []),
            discard=d.get("discard", []),
            deckCount=d.get("deckCount", 60),
        )
