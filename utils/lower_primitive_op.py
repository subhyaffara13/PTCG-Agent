
def lower_primitive_op(name: str) -> Callable[[LF], LF]:
    """Register a handler that generates low-level IR for a primitive op."""

    def wrapper(f: LF) -> LF:
        assert name not in lowering_registry
        lowering_registry[name] = f
        return f

    return wrapper

