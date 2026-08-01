
def free_symbols(val: IterateExprs) -> OrderedSet[sympy.Symbol]:
    """
    Recursively collect all free symbols from a value.

    This function traverses various data structures (tensors, lists, tuples, etc.) and extracts
    all sympy symbols contained within them. It's useful for finding all symbolic variables
    that a complex nested structure depends on.

    Args:
        val: The value to extract symbols from. Can be a symbolic type (SymInt, SymFloat, SymBool),
             a container (tuple, list), a tensor, or None.

    Returns:
        OrderedSet[sympy.Symbol]: An ordered set of all free symbols found in the value.
    """
    if val is None:
        return OrderedSet()

    itr = _iterate_exprs(val)

    # we need at least 1 to call union, so we hand code the identity
    try:
        first_expr = next(itr)
    except StopIteration:
        return OrderedSet()

    # TODO: Apparently, returning an OrderedSet here breaks
    # python test/distributed/tensor/test_dtensor_compile.py TestDTensorCompile.test_dtensor_dynamic
    return first_expr.free_symbols.union(*(e.free_symbols for e in itr))  # type: ignore[return-value]

