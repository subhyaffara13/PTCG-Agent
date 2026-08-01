
def _create_nested_fn(
    code: types.CodeType,
    f_globals: dict[str, Any],
    name: str,
    defaults: tuple[object, ...] | None,
    closure: tuple[CellType] | None,
    kwdefaults: dict[str, Any] | None,
    annotations: dict[str, Any] | None,
) -> types.FunctionType:
    from types import FunctionType

    func = FunctionType(code, f_globals, name, defaults, closure)
    func.__kwdefaults__ = kwdefaults

    if isinstance(annotations, tuple):
        from itertools import pairwise

        annotations = dict(pairwise(annotations))

    # TypeError: __annotations__ must be set to a dict object
    assert annotations is None or isinstance(annotations, dict)
    func.__annotations__ = annotations  # type: ignore[assignment]

    return func

