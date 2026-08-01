
def unimplemented_with_warning(
    e: Exception,
    code: types.CodeType,
    *,
    gb_type: str,
    context: str,
    explanation: str,
    hints: list[str],
) -> NoReturn:
    # This function calls unimplemented internally and eventually graph breaks
    # or falls to eager. unimplemented itself does not print any user warnings,
    # i.e., its very silent. This helper function is intended when an error is
    # encountered in the torch.compile stack which is worth showing as warning
    # to the user. For example, if AOT Autograd backend fails with a fake tensor
    # exception, its ok to fallback to eager but not silently. Here, we can use
    # this function to log the message and the stack trace.
    graph_break_msg = format_error_msg_verbose(e, code)
    torch._logging.trace_structured(
        "artifact",
        metadata_fn=lambda: {
            "name": "dynamo_graph_break_reason",
            "encoding": "string",
        },
        payload_fn=lambda: graph_break_msg,
    )
    graph_breaks_log.debug("%s", graph_break_msg)
    _unimplemented = unimplemented
    # to prevent a graph break registry entry
    _unimplemented(
        gb_type=gb_type,
        context=context,
        explanation=explanation,
        hints=hints,
        from_exc=e,
        log_warning=True,
    )

