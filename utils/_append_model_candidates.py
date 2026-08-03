from typing import Any, List

def _append_model_candidates(candidates: List[str], value: Any) -> None:
    if value is None:
        return

    values = value if isinstance(value, (list, tuple, set)) else [value]
    for item in values:
        if item is None:
            continue
        if isinstance(item, str):
            model_names = [model.strip() for model in item.split(",")]
        else:
            model_names = [str(item).strip()]
        candidates.extend(model for model in model_names if model)

