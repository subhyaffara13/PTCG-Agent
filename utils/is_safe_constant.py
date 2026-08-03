from typing import Any

def is_safe_constant(v: Any) -> bool:
    if istype(v, (tuple, frozenset)):
        return all(map(is_safe_constant, v))
    return isinstance(
        v,
        (
            enum.Enum,
            type,
            torch.Size,
            typing._GenericAlias,  # type: ignore[attr-defined]
            types.GenericAlias,
        ),
    ) or istype(
        v,
        common_constant_types | {slice},
    )

