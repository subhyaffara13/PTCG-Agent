import json
from typing import Any

def _compiler_config_for_logging() -> str | None:
    def clean_for_json(d: dict[str, Any]) -> dict[str, Any]:
        blocklist = {
            "TYPE_CHECKING",
        }

        return {
            key: sorted(value) if isinstance(value, set) else value
            for key, value in d.items()
            if key not in blocklist
        }

    if not torch.compiler.config:
        return None

    try:
        compiler_config_copy = torch.compiler.config.get_config_copy()  # type: ignore[attr-defined]
    except (TypeError, AttributeError):
        return "Compiler Config cannot be pickled"

    config_dict = clean_for_json(compiler_config_copy)
    return json.dumps(config_dict, sort_keys=True)

