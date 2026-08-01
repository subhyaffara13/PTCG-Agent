
def get_all_dsls() -> list[str]:
    """Get all registered DSL names (available or not) for comprehensive testing"""
    return _dsl_checker.list_all()

