from typing import Any

def _create_named_tuple(
    t,
    unqual_name: str,
    field_names: list[str],
    defaults: tuple[Any, ...],
):
    TupleType = collections.namedtuple(unqual_name, field_names, defaults=defaults)  # type: ignore[call-arg, no-redef, misc]
    return TupleType(*t)

