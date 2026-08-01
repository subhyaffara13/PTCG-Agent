
def _formatdef(func: Callable[..., object]) -> str:
    return f"{func.__name__}{inspect.signature(func)}"

