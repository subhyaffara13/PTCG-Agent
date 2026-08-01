
def is_collection_argument_subsumed_by(
    arg: CollectionArgument, by: CollectionArgument
) -> bool:
    """Check if `arg` is subsumed (contained) by `by`."""
    # First check path subsumption.
    if by.path != arg.path:
        # `by` subsumes `arg` if `by` is a parent directory of `arg` and has no
        # parts (collects everything in that directory).
        if not by.parts:
            return arg.path.is_relative_to(by.path)
        return False
    # Paths are equal, check parts.
    # For example: ("TestClass",) is a prefix of ("TestClass", "test_method").
    if len(by.parts) > len(arg.parts) or arg.parts[: len(by.parts)] != by.parts:
        return False
    # Paths and parts are equal, check parametrization.
    # A `by` without parametrization (None) matches everything, e.g.
    # `pytest x.py::test_it` matches `x.py::test_it[0]`. Otherwise must be
    # exactly equal.
    if by.parametrization is not None and by.parametrization != arg.parametrization:
        return False
    return True

