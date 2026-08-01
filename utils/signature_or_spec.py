
def signature_or_spec(func):
    try:
        return inspect.signature(func)
    except (ValueError, TypeError):
        return None

