import json
import os
import time
from typing import Any

def _write_status(status_dir: str, cell: GameCell, state: str,
                  started_at: float, **extra: Any) -> None:
    """Atomically write a per-cell status snapshot.

    Workers call this on each agent invocation so the parent's monitor
    thread can show move-by-move progress for in-flight games.
    """
    if not status_dir:
        return
    path = os.path.join(status_dir, _status_filename(cell))
    payload = {
        "variant": cell.variant,
        "model_p0": cell.model_p0,
        "model_p1": cell.model_p1,
        "seed": cell.seed,
        "pair_role": cell.pair_role,
        "state": state,
        "started_at": started_at,
        "updated_at": time.time(),
        **extra,
    }
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(payload, f)
    os.replace(tmp, path)

