
def _assert_attr_equal(attr: str, left, right, obj: str = "Attributes"):
    """
    patch tm.assert_attr_equal so NumpyEADtype("object") is closed enough to
    np.dtype("object")
    """
    if attr == "dtype":
        lattr = getattr(left, "dtype", None)
        rattr = getattr(right, "dtype", None)
        if isinstance(lattr, NumpyEADtype) and not isinstance(rattr, NumpyEADtype):
            left = left.astype(lattr.numpy_dtype)
        elif isinstance(rattr, NumpyEADtype) and not isinstance(lattr, NumpyEADtype):
            right = right.astype(rattr.numpy_dtype)

    orig_assert_attr_equal(attr, left, right, obj)

