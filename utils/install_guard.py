import logging

def install_guard(*guards: Guard, skip: int = 0) -> None:
    """
    Add dynamo guards to the current tracing context.

    Args:
        guards: guard(s) to add
        skip: number of stack frames to ignore for debug stack trace
    """
    from torch._guards import TracingContext

    guards_context = TracingContext.get().guards_context
    if guards_context.skip_install:
        return

    collect_debug_stack = guards_log.isEnabledFor(
        logging.DEBUG
    ) or verbose_guards_log.isEnabledFor(logging.DEBUG)
    add = guards_context.dynamo_guards.add
    for guard in guards:
        assert isinstance(guard, Guard)
        if is_from_skip_guard_source(guard.originating_source):
            continue
        add(guard, collect_debug_stack=collect_debug_stack, skip=skip + 1)

