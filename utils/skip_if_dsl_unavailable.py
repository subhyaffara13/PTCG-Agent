
def skipIfDSLUnavailable(dsl_name: str, reason: str | None = None):
    """Skip test if specific DSL is not available"""
    available = _dsl_checker.is_available(dsl_name)
    msg = reason or f"{dsl_name} DSL not available"
    return unittest.skipIf(not available, msg)

