
def skipUnlessDSLAvailable(dsl_name: str, reason: str | None = None):
    """Skip test unless specific DSL is available"""
    available = _dsl_checker.is_available(dsl_name)
    msg = reason or f"{dsl_name} DSL required"
    return unittest.skipUnless(available, msg)

