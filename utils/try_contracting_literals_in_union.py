import itertools
from typing import Any

def try_contracting_literals_in_union(types: Sequence[Type]) -> list[ProperType]:
    """Contracts any literal types back into a sum type if possible.

    Requires a flattened union and does not descend into children.

    Will replace the first instance of the literal with the sum type and
    remove all others.

    If we call `try_contracting_union(Literal[Color.RED, Color.BLUE, Color.YELLOW])`,
    this function will return Color.

    We also treat `Literal[True, False]` as `bool`.
    """
    proper_types = [get_proper_type(typ) for typ in types]
    sum_types: dict[str, tuple[set[Any], list[int]]] = {}
    marked_for_deletion = set()
    for idx, typ in enumerate(proper_types):
        if isinstance(typ, LiteralType):
            fullname = typ.fallback.type.fullname
            if typ.fallback.type.is_enum or isinstance(typ.value, bool):
                if fullname not in sum_types:
                    sum_types[fullname] = (
                        (
                            set(typ.fallback.type.enum_members)
                            if typ.fallback.type.is_enum
                            else {True, False}
                        ),
                        [],
                    )
                literals, indexes = sum_types[fullname]
                literals.discard(typ.value)
                indexes.append(idx)
                if not literals:
                    first, *rest = indexes
                    proper_types[first] = typ.fallback
                    marked_for_deletion |= set(rest)
    return list(
        itertools.compress(
            proper_types, [(i not in marked_for_deletion) for i in range(len(proper_types))]
        )
    )

