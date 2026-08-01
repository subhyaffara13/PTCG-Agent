
def _set_in_optimized_module() -> Generator[None, None, None]:
    # Set in dynamo's OptimizedModule forward, to have better coverage than is_compiling().
    # Prevents graph-breaking forward hooks from being registered & traced.
    # TODO(pianpwk): subsume this flag with better is_compiling() coverage
    global _in_optimized_module
    _old_in_optimized_module = (
        _in_optimized_module  # do we need this? can we just set it to False after
    )
    _in_optimized_module = True
    try:
        yield
    finally:
        _in_optimized_module = _old_in_optimized_module

