from typing import Any, Dict, List

def _accumulate_breakdown(
    results: List[Dict[str, Any]], dimension: str, fields: List[str]
) -> Dict[str, Dict[str, float]]:
    """Aggregate a single breakdown dimension across days."""
    totals: Dict[str, Dict[str, float]] = {}
    for day in results:
        for key, entry in day.get("breakdown", {}).get(dimension, {}).items():
            if key not in totals:
                totals[key] = {f: 0.0 for f in fields}
            m = entry.get("metrics", {})
            for f in fields:
                totals[key][f] += m.get(f, 0)
    return totals

