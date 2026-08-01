
def reset_audit_log_callback_cache() -> None:
    """Clear cached audit-log callback instances. Call on config reload."""
    _audit_log_callback_cache.clear()

