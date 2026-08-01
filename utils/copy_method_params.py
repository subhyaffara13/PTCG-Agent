
def copy_method_params(
    source_method: Callable[Concatenate[Any, _P], Any],
) -> Callable[[Callable[..., _R]], Callable[Concatenate[_A1, _P], _R]]:
    """Cast the decorated *method*'s call signature to the source_method's.
    Keeps the first argument type (e.g., self/cls).
    """

    def return_func(func: Callable[..., _R]) -> Callable[Concatenate[_A1, _P], _R]:
        return cast(Callable[Concatenate[_A1, _P], _R], func)

    return return_func

