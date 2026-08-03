from typing import Any

def _format_dict(
    attr: dict[Any, Any],
    indent: int,
    width: int,
    curr_indent: int,
) -> str:
    curr_indent += indent + 3
    dict_repr = []
    for k, v in attr.items():
        k_repr = repr(k)
        v_str = (
            pformat(v, indent, width, curr_indent + len(k_repr))
            if is_dataclass(v)
            else repr(v)
        )
        dict_repr.append(f"{k_repr}: {v_str}")

    return _format(dict_repr, indent, width, curr_indent, "{", "}")


def _format_dict(d: dict) -> str:
    return "\n".join([f"- {prop}: {val}" for prop, val in d.items()]) + "\n"

