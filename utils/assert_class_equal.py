
def assert_class_equal(
    left, right, exact: bool | str = True, obj: str = "Input"
) -> None:
    """
    Checks classes are equal.
    """
    __tracebackhide__ = True

    def repr_class(x):
        if isinstance(x, Index):
            # return Index as it is to include values in the error message
            return x

        return type(x).__name__

    def is_class_equiv(idx: Index) -> bool:
        """Classes that are a RangeIndex (sub-)instance or exactly an `Index` .

        This only checks class equivalence. There is a separate check that the
        dtype is int64.
        """
        return type(idx) is Index or isinstance(idx, RangeIndex)

    if type(left) == type(right):
        return

    if exact == "equiv":
        if is_class_equiv(left) and is_class_equiv(right):
            return

    msg = f"{obj} classes are different"
    raise_assert_detail(obj, msg, repr_class(left), repr_class(right))

