
def performance_warning(request) -> Iterator[bool | type[Warning]]:
    """
    Fixture to check if performance warnings are enabled. Either produces
    ``PerformanceWarning`` if they are enabled, otherwise ``False``.
    """
    with pd.option_context("mode.performance_warnings", request.param):
        yield pd.errors.PerformanceWarning if request.param else False

