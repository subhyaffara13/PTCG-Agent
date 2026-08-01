
def should_suppress_spend_log_tracebacks() -> bool:
    """Return ``True`` when spend-log traceback suppression should apply.

    Suppression only kicks in when both:
      * the operator opted in via the env var, and
      * the proxy logger is at INFO or above (i.e. not DEBUG) — at DEBUG we
        still want full tracebacks for troubleshooting.
    """
    if not _is_suppression_env_enabled():
        return False
    return not verbose_proxy_logger.isEnabledFor(logging.DEBUG)

