
def dtrace_structured(
    name: str,
    # NB: metadata expected to be dict so adding more info is forward compatible
    # Tuple[str, int] is a special case for string interning
    metadata_fn: Callable[[], dict[str, Any] | tuple[str, int]] = dict,
    *,
    payload_fn: Callable[[], str | object | None] = lambda: None,
    suppress_context: bool = False,
    expect_trace_id: bool = False,  # Whether or not we expect to have a current trace id
    record_logging_overhead: bool = True,  # Whether or not to record the time spent on structured logging
) -> None:
    """
    For logging more detailed information used for debugging. This may result in
    the program becoming slow.
    """
    if GET_DTRACE_STRUCTURED:
        trace_structured(
            name,
            metadata_fn,
            payload_fn=payload_fn,
            suppress_context=suppress_context,
            expect_trace_id=expect_trace_id,
            record_logging_overhead=record_logging_overhead,
        )

