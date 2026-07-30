from typing import Dict, Any, Optional

from dataclasses import dataclass, field
from typing import Dict, Any, Optional

@dataclass
class GameConfig:
    iteration_id: int
    version_a: str
    version_b: str
    deck_a: Any = None
    deck_b: Any = None
    reasoning_a: dict = field(default_factory=dict)
    reasoning_b: dict = field(default_factory=dict)
    label: str = ""

@dataclass
class GameResult:
    config: GameConfig
    result: Optional[Dict[str, Any]] = None
    success: bool = True
    error: str = ""
