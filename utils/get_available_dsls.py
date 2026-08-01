
def get_available_dsls() -> list[str]:
    """Get list of available DSL names for test parameterization"""
    return _dsl_checker.list_available()

