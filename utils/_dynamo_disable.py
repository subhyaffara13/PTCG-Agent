import functools

def _dynamo_disable(func):
    """Disable dynamo tracing for FSDP hooks."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return torch._dynamo.disable(
            func, recursive=True, reason="skipping FSDP hooks"
        )(*args, **kwargs)

    return wrapper

