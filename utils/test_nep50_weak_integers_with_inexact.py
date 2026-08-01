
def test_nep50_weak_integers_with_inexact(dtype):
    # Avoids warning (different code path for scalars)
    scalar_type = np.dtype(dtype).type

    too_big_int = int(np.finfo(dtype).max) * 2

    if dtype in "dDG":
        # These dtypes currently convert to Python float internally, which
        # raises an OverflowError, while the other dtypes overflow to inf.
        # NOTE: It may make sense to normalize the behavior!
        with pytest.raises(OverflowError):
            scalar_type(1) + too_big_int

        with pytest.raises(OverflowError):
            np.array(1, dtype=dtype) + too_big_int
    else:
        # NumPy uses (or used) `int -> string -> longdouble` for the
        # conversion.  But Python may refuse `str(int)` for huge ints.
        # In that case, RuntimeWarning would be correct, but conversion
        # fails earlier (seems to happen on 32bit linux, possibly only debug).
        if dtype in "gG":
            try:
                str(too_big_int)
            except ValueError:
                pytest.skip("`huge_int -> string -> longdouble` failed")

        # Otherwise, we overflow to infinity:
        with pytest.warns(RuntimeWarning):
            res = scalar_type(1) + too_big_int
        assert res.dtype == dtype
        assert res == np.inf

        with pytest.warns(RuntimeWarning):
            # We force the dtype here, since windows may otherwise pick the
            # double instead of the longdouble loop.  That leads to slightly
            # different results (conversion of the int fails as above).
            res = np.add(np.array(1, dtype=dtype), too_big_int, dtype=dtype)
        assert res.dtype == dtype
        assert res == np.inf

