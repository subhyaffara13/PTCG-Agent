
def copy_type(t: ProperType) -> ProperType:
    """Create a shallow copy of a type.

    This can be used to mutate the copy with truthiness information.

    Classes compiled with mypyc don't support copy.copy(), so we need
    a custom implementation.
    """
    return t.accept(TypeShallowCopier())

