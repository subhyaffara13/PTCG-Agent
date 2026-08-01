
def _isolation_context(
    ischema: IsolationSchema = _DEFAULT_ISOLATION_SCHEMA,
) -> dict[str, object]:
    """Generate context data based on the isolation schema.

    Args:
        ischema: Schema specifying which context forms to include.
                Defaults to including all runtime and compile context.

    Returns:
        A dictionary containing the selected context data with keys
        "runtime_context" and "compile_context", where each value is
        either None (if excluded) or a dict of context form data.
    """
    return {
        "runtime_context": _collect_runtime_context(ischema["runtime_context"]),
        "compile_context": _collect_compile_context(ischema["compile_context"]),
    }

