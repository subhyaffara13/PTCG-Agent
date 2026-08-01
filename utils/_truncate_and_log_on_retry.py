
def _truncate_and_log_on_retry(retry_state: tenacity.RetryCallState):
    """
    Tenacity hook called before a retry. It reduces the context size if a
    RateLimitError was detected.
    """
    # The first argument of the retried method is the class instance 'self'
    agent_instance = retry_state.args[0]

    if _is_rate_limit_error(retry_state.outcome.exception()):
        # Reduce the number of history items to keep by 25% on each attempt
        original_count = agent_instance._event_log_items_to_keep
        agent_instance._event_log_items_to_keep = int(original_count * 0.75)

        logger.warning(
            "ContextWindowExceededError detected. Retrying with smaller context. "
            "Reducing event log from %d to %d itms.",
            original_count,
            agent_instance._event_log_items_to_keep,
        )

    # Also call the original logging function for general retry logging
    _log_retry_warning(retry_state)

