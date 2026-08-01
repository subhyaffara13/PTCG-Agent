
def _is_suppression_env_enabled() -> bool:
    """Read the opt-in env var fresh each call so dynamic flips are honored.

    Kept separate from ``should_suppress_spend_log_tracebacks`` so tests and
    other call sites can introspect just the env-var state without also
    consulting the live logger level.
    """
    return str_to_bool(os.getenv(SUPPRESS_SPEND_LOG_TRACEBACKS_ENV)) is True

