
def _is_target_model_names_key(key: str) -> bool:
    return key == "target_model_names" or (
        key.startswith("target_model_names[") and key.endswith("]")
    )

