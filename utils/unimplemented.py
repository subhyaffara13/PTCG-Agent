
def unimplemented(
    *,
    gb_type: str,
    context: str,
    explanation: str,
    hints: list[str],
    from_exc: Any = _NOTHING,
    log_warning: bool = False,
    skip_frame: bool = False,
) -> NoReturn:
    """
    Called within dynamo to cause a graph break.
    Args:
        gb_type: Context-free graph break type. It should be a short string without any
                 information specific to the tracing context (i.e. no dynamically-generated strings)
        context: Developer context for the graph break. It can contain tracing context/dynamic strings.
        explanation: User-facing context-dependent explanation for the graph break. Can be dynamic.
        hints: List of user-facing hints for the graph break.
    """

    msg = format_graph_break_message(gb_type, context, explanation, hints)

    if log_warning:
        log.warning(msg)
    if from_exc is not _NOTHING:
        past_real_stack = None
        if hasattr(from_exc, "real_stack"):
            past_real_stack = from_exc.real_stack
        if isinstance(from_exc, Unsupported):
            msg = f"{from_exc.msg}\n\n*** While handling this graph break, another graph break occurred: ***\n\n{msg}"
            # noqa: GB_REGISTRY
            raise Unsupported(msg, gb_type, skip_frame, real_stack=past_real_stack)
        # noqa: GB_REGISTRY
        raise Unsupported(
            msg, gb_type, skip_frame, real_stack=past_real_stack
        ) from from_exc
    # noqa: GB_REGISTRY
    raise Unsupported(msg, gb_type, skip_frame)

