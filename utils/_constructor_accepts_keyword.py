
def _constructor_accepts_keyword(constructor: Callable[..., object], name: str) -> bool:
    try:
        parameters = inspect.signature(constructor).parameters
    except (TypeError, ValueError):
        return False

    return name in parameters or any(
        parameter.kind is inspect.Parameter.VAR_KEYWORD for parameter in parameters.values()
    )

