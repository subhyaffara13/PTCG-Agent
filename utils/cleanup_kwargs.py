
def cleanup_kwargs(**kwargs):
    """
    Remove unsupported or disabled keys from kwargs
    """
    connection_kwargs = {
        k: v
        for k, v in kwargs.items()
        if k in REDIS_ALLOWED_KEYS and k not in KWARGS_DISABLED_KEYS
    }

    return connection_kwargs

