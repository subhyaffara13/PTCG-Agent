import copy
from typing import Any, Callable

def _transform_callback_vars(
    metadata: Any, transform: Callable[[str, Any], Any]
) -> Any:
    if not isinstance(metadata, dict):
        return metadata
    out = copy.deepcopy(metadata)
    logging_entries = out.get("logging")
    if isinstance(logging_entries, list):
        for entry in logging_entries:
            if isinstance(entry, dict) and isinstance(entry.get("callback_vars"), dict):
                entry["callback_vars"] = {
                    k: transform(k, v) for k, v in entry["callback_vars"].items()
                }
    callback_settings = out.get("callback_settings")
    if isinstance(callback_settings, dict) and isinstance(
        callback_settings.get("callback_vars"), dict
    ):
        callback_settings["callback_vars"] = {
            k: transform(k, v) for k, v in callback_settings["callback_vars"].items()
        }
    return out

