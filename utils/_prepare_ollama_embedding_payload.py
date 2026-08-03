from typing import Any, Dict, List

def _prepare_ollama_embedding_payload(
    model: str, prompts: List[str], optional_params: Dict[str, Any]
) -> Dict[str, Any]:
    data: Dict[str, Any] = {"model": model, "input": prompts}
    special_optional_params = ["truncate", "options", "keep_alive", "dimensions"]

    for k, v in optional_params.items():
        if k in special_optional_params:
            data[k] = v
        else:
            data.setdefault("options", {})
            if isinstance(data["options"], dict):
                data["options"].update({k: v})
    return data

