from typing import Callable, Dict, List

def _ranked_lines(
    totals: Dict[str, Dict[str, float]],
    fmt: Callable[[str, Dict[str, float]], str],
    limit: int,
) -> List[str]:
    """Sort by spend descending, format each entry, and truncate."""
    return [
        fmt(name, vals)
        for name, vals in sorted(totals.items(), key=lambda x: -x[1].get("spend", 0))[
            :limit
        ]
    ]

