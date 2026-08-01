
def is_simple_refcounted_pointer(rtype: RType) -> bool:
    """Is rtype represented at runtime as a single, reference-counted 'PyObject *'?

    This covers 'object', 'str', containers, instances of native classes and
    optional/union types -- everything whose C representation is exactly one
    'PyObject *' field that owns a reference. It excludes unboxed types (tagged
    'int', fixed-width ints, floats, bools), inline tuples ('RTuple'), vectors
    ('RVec') and C structs ('RStruct'), which need different treatment for
    free-threaded memory safety.
    """
    return rtype.is_refcounted and not rtype.is_unboxed and not isinstance(rtype, RStruct)

