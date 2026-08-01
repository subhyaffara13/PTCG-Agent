
def phase_handler(phase: DetailedPhase):
    """Decorator to register a method as a handler for a specific game phase."""

    def decorator(func):
        setattr(func, "_phase_handler_for", phase)
        return func

    return decorator

