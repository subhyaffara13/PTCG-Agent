from typing import Any

def specification_with(
    dialect_id: URI,
    default: Specification[Any] | _Unset = _UNSET,
) -> Specification[Any]:
    """
    Retrieve the `Specification` with the given dialect identifier.

    Raises:

        `UnknownDialect`

            if the given ``dialect_id`` isn't known

    """
    resource = _SPECIFICATIONS.get(dialect_id.rstrip("#"))
    if resource is not None:
        return resource.contents
    if default is _UNSET:
        raise UnknownDialect(dialect_id)
    return default

