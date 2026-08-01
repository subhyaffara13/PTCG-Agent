
def _concrete_value(val: None | int | SymInt) -> int:
    """Get the concrete int value for a non-symbolic size/stride entry.

    Used for entries that are NOT symbolic placeholders, meaning they are
    concrete ints or nested ints (represented as -1 after make_runtime_safe).
    """
    if isinstance(val, int):
        return val
    # Before make_runtime_safe: nested ints are SymInts; use -1 as dummy.
    # After make_runtime_safe: they're already -1.
    if isinstance(val, SymInt) and val.node.is_nested_int():
        return -1
    raise AssertionError(f"Expected concrete int, got {type(val)}: {val}")

