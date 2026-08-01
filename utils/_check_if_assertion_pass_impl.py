
def _check_if_assertion_pass_impl() -> bool:
    """Check if any plugins implement the pytest_assertion_pass hook
    in order not to generate explanation unnecessarily (might be expensive)."""
    return True if util._assertion_pass else False

