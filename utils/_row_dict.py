from typing import Any

def _row_dict(r: GameResult) -> dict[str, Any]:
    return dataclasses.asdict(r)

