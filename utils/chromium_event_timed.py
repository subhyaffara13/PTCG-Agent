import time
from typing import Any

def chromium_event_timed(
    event_name: str,
    reset_event_log_on_exit: bool = False,
    log_pt2_compile_event: bool = False,
) -> Generator[Any, None, None]:
    """
    Context manager that creates a chromium start and end event. Chromium event
    logging is integrated with dynamo_timed, so you probably want to use that
    instead. Use this context manager only if you want to avoid dynamo_timed.
    """
    chromium_event_log = get_chromium_event_logger()
    chromium_start_time = time.time_ns()
    chromium_event_log.log_event_start(
        event_name,
        chromium_start_time,
        {},
        log_pt2_compile_event,
    )
    try:
        yield
    finally:
        chromium_event_log.log_event_end(
            event_name,
            time.time_ns(),
            {},
            chromium_start_time,
            log_pt2_compile_event,
        )
        if reset_event_log_on_exit:
            chromium_event_log.reset()

