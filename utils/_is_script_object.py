from typing import Any

def _is_script_object(obj: Any) -> bool:
    return isinstance(
        obj, torch.ScriptObject
    ) and obj._type().qualified_name().startswith(  # type: ignore[attr-defined]
        "__torch__.torch.classes"
    )

