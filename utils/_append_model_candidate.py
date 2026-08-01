
def _append_model_candidate(candidates: list[str], model: Any) -> None:
    if isinstance(model, str) and model and model not in candidates:
        candidates.append(model)

