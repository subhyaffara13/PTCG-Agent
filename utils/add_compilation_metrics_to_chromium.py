
def add_compilation_metrics_to_chromium(c: CompilationMetrics) -> None:
    """
    These are the common fields in CompilationMetrics that existed before
    metrics_context, and aren't set by MetricsContext.set(). We add the subset
    of them that make sense in `dynamo`/toplevel events in PT2 Compile Events
    directly.

    If you're tempted to add to this list, consider using CompileEventLogger.compilation_metric()
    instead, which will automatically also add it to tlparse and PT2 Compile Events.
    TODO: Get rid of this function and replace it with CompileEventLogger directly instead.
    """
    event_logger = get_chromium_event_logger()
    event_name = event_logger.get_outermost_event()
    if not event_name:
        return
    event_logger.add_event_data(
        event_name=event_name,
        frame_key=c.frame_key,
        co_name=c.co_name,
        co_filename=c.co_filename,
        co_firstlineno=c.co_firstlineno,
        cache_size=c.cache_size,
        accumulated_cache_size=c.accumulated_cache_size,
        guard_count=c.guard_count,
        shape_env_guard_count=c.shape_env_guard_count,
        graph_op_count=c.graph_op_count,
        graph_node_count=c.graph_node_count,
        graph_input_count=c.graph_input_count,
        fail_type=c.fail_type,
        fail_reason=c.fail_reason,
        fail_user_frame_filename=c.fail_user_frame_filename,
        fail_user_frame_lineno=c.fail_user_frame_lineno,
        # Sets aren't JSON serializable
        non_compliant_ops=(
            list(c.non_compliant_ops) if c.non_compliant_ops is not None else None
        ),
        compliant_custom_ops=(
            list(c.compliant_custom_ops) if c.compliant_custom_ops is not None else None
        ),
        restart_reasons=(
            list(c.restart_reasons) if c.restart_reasons is not None else None
        ),
        dynamo_time_before_restart_s=c.dynamo_time_before_restart_s,
        has_guarded_code=c.has_guarded_code,
        dynamo_config=c.dynamo_config,
    )

