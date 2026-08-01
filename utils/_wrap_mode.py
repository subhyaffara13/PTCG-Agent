
def _wrap_mode(function: Callable[..., str]) -> Callable[..., str]:
    """Registers an individual wrap mode. Function name and order are significant and used for
    creating enum.
    """
    _wrap_modes[function.__name__.upper()] = function
    function.__signature__ = signature(_wrap_mode_interface)  # type: ignore
    function.__annotations__ = _wrap_mode_interface.__annotations__
    return function

