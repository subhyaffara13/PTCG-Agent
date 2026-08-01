
def axis(
    arg: tuple[float, float, float, float] | bool | str | None = None,
    /,
    *,
    emit: bool = True,
    **kwargs,
) -> tuple[float, float, float, float]:
    return gca().axis(arg, emit=emit, **kwargs)


def axis(request):
    """
    Fixture for returning the axis numbers of a DataFrame.
    """
    return request.param

