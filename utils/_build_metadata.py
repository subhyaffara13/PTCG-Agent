from typing import Any

def _build_metadata(extra_meta):
    fields: dict[str, Any] = {}
    any_populated = False
    for kineto_key, (field_name, convert) in _EVENT_METADATA_KEYS.items():
        v = extra_meta.get(kineto_key)
        if v is not None:
            fields[field_name] = convert(v)
            any_populated = True
        else:
            fields[field_name] = None
    return EventMetadata(**fields) if any_populated else None

