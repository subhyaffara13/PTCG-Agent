
def get_is_bisection_enabled() -> bool:
    return (
        CompilerBisector.get_subsystem() is not None
        or CompilerBisector.get_backend() is not None
    )

