
def serialTest(condition=True):
    """
    Decorator for running tests serially.  Requires pytest
    """
    # If one apply decorator directly condition will be callable
    # And test will essentially be essentially skipped, which is undesirable
    if type(condition) is not bool:
        raise AssertionError(f"expected condition to be bool, got {type(condition)}")

    def decorator(fn):
        if has_pytest and condition:
            return pytest.mark.serial(fn)
        return fn
    return decorator

