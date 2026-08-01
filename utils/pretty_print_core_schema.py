
def pretty_print_core_schema(
    val: Any,
    *,
    console: Console | None = None,
    max_depth: int | None = None,
    strip_metadata: bool = True,
) -> None:  # pragma: no cover
    """Pretty-print a core schema using the `rich` library.

    Args:
        val: The core schema to print, or a Pydantic model/dataclass/type adapter
            (in which case the cached core schema is fetched and printed).
        console: A rich console to use when printing. Defaults to the global rich console instance.
        max_depth: The number of nesting levels which may be printed.
        strip_metadata: Whether to strip metadata in the output. If `True` any known core metadata
            attributes will be stripped (but custom attributes are kept). Defaults to `True`.
    """
    # lazy import:
    from rich.pretty import pprint

    # circ. imports:
    from pydantic import BaseModel, TypeAdapter
    from pydantic.dataclasses import is_pydantic_dataclass

    if (inspect.isclass(val) and issubclass(val, BaseModel)) or is_pydantic_dataclass(val):
        val = val.__pydantic_core_schema__
    if isinstance(val, TypeAdapter):
        val = val.core_schema
    cleaned_schema = _clean_schema_for_pretty_print(val, strip_metadata=strip_metadata)

    pprint(cleaned_schema, console=console, max_depth=max_depth)

