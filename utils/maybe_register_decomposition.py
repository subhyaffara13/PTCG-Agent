
def maybe_register_decomposition(op):
    def decorator(f):
        try:
            return register_decomposition(op)(f)
        except Exception:
            return f

    return decorator

