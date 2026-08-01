
def _log_retry_warning(retry_state: tenacity.RetryCallState):
    assert retry_state.outcome is not None
    exception = retry_state.outcome.exception()
    traceback_str = "".join(traceback.format_exception(exception))
    if retry_state.attempt_number < 1:
        loglevel = logging.INFO
    else:
        loglevel = logging.WARNING
    logging.log(
        loglevel,
        "Retrying: $s attempt # %s ended with: $s Traceback: %s Retry state: %s",
        retry_state.fn,
        retry_state.attempt_number,
        retry_state.outcome,
        traceback_str,
        retry_state,
    )

