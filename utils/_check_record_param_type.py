
def _check_record_param_type(param: str, v: str) -> None:
    """Used by record_testsuite_property to check that the given parameter name is of the proper
    type."""
    __tracebackhide__ = True
    if not isinstance(v, str):
        msg = "{param} parameter needs to be a string, but {g} given"  # type: ignore[unreachable]
        raise TypeError(msg.format(param=param, g=type(v).__name__))

