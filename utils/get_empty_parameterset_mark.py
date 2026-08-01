
def get_empty_parameterset_mark(
    config: Config, argnames: Sequence[str], func
) -> MarkDecorator:
    from ..nodes import Collector

    argslisting = ", ".join(argnames)

    _fs, lineno = getfslineno(func)
    reason = f"got empty parameter set for ({argslisting})"
    requested_mark = config.getini(EMPTY_PARAMETERSET_OPTION)
    if requested_mark in ("", None, "skip"):
        mark = MARK_GEN.skip(reason=reason)
    elif requested_mark == "xfail":
        mark = MARK_GEN.xfail(reason=reason, run=False)
    elif requested_mark == "fail_at_collect":
        raise Collector.CollectError(
            f"Empty parameter set in '{func.__name__}' at line {lineno + 1}"
        )
    else:
        raise LookupError(requested_mark)
    return mark

