from typing import Any, Dict, List
import math


def _conditionSetFrom(conditionSet: List[Dict[str, Any]]) -> ConditionSet:
    c: Dict[str, Range] = {}
    for condition in conditionSet:
        minimum, maximum = condition.get("minimum"), condition.get("maximum")
        c[condition["name"]] = Range(
            minimum if minimum is not None else -math.inf,
            maximum if maximum is not None else math.inf,
        )
    return c

