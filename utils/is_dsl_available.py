
def is_dsl_available(dsl_name: str) -> bool:
    """Check if specific DSL is available for conditional testing"""
    return _dsl_checker.is_available(dsl_name)

