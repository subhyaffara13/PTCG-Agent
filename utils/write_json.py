import json
from typing import Any

def write_json(data: WriteBuffer, value: dict[str, Any]) -> None:
    write_tag(data, DICT_STR_GEN)
    write_int_bare(data, len(value))
    for key in sorted(value):
        write_str_bare(data, key)
        write_json_value(data, value[key])


def write_json(obj: Mapping[str, Any], path: str, **kwargs) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, **kwargs)


def write_json(obj, path, **kwargs):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, **kwargs)

