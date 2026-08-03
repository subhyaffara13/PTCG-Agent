from typing import Any, Optional

def extract_model_from_target_model_names(target_model_names: Any) -> Optional[str]:
    if isinstance(target_model_names, str):
        target_model_names = [
            m.strip() for m in target_model_names.split(",") if m.strip()
        ]
    elif not isinstance(target_model_names, list):
        return None
    return target_model_names[0] if target_model_names else None

