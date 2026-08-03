from typing import Any

def _format_list(
    attr: list[Any] | set[Any] | tuple[Any, ...],
    indent: int,
    width: int,
    curr_indent: int,
) -> str:
    curr_indent += indent + 1
    list_repr = [
        pformat(l, indent, width, curr_indent) if is_dataclass(l) else repr(l)
        for l in attr
    ]
    start, end = ("[", "]") if isinstance(attr, list) else ("(", ")")
    return _format(list_repr, indent, width, curr_indent, start, end)

