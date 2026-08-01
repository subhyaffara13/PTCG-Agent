
def _add_error_entry_on_retry(retry_state: tenacity.RetryCallState):
    last_exception_wrapper = retry_state.outcome.exception()
    if isinstance(last_exception_wrapper, LLMActionException):
        last_exception = last_exception_wrapper.original_exception
        # You can also access the failed output here if needed for logging
        raw_out = last_exception_wrapper.raw_out
        prompt = last_exception_wrapper.prompt
        logger.warning(f"Retrying due to JSON parsing error. Failed output: {raw_out} Failed prompt: {prompt}")
    else:
        last_exception = last_exception_wrapper

    stack_trace_list = traceback.format_exception(last_exception)
    stack_trace_str = "".join(stack_trace_list)
    retry_state.kwargs["error_stack_trace"] = stack_trace_str
    _log_retry_warning(retry_state)

