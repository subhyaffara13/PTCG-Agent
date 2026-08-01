
def test_is_extension_array_dtype(check_scipy):
    assert not com.is_extension_array_dtype([1, 2, 3])
    assert not com.is_extension_array_dtype(np.array([1, 2, 3]))
    assert not com.is_extension_array_dtype(pd.DatetimeIndex([1, 2, 3]))

    cat = pd.Categorical([1, 2, 3])
    assert com.is_extension_array_dtype(cat)
    assert com.is_extension_array_dtype(pd.Series(cat))
    assert com.is_extension_array_dtype(SparseArray([1, 2, 3]))
    assert com.is_extension_array_dtype(pd.DatetimeIndex(["2000"], tz="US/Eastern"))

    dtype = DatetimeTZDtype("ns", tz="US/Eastern")
    s = pd.Series([], dtype=dtype)
    assert com.is_extension_array_dtype(s)

    if check_scipy:
        import scipy.sparse

        assert not com.is_extension_array_dtype(scipy.sparse.bsr_matrix([1, 2, 3]))


def test_is_extension_array_dtype(dtype):
    assert isinstance(dtype, dtypes.ExtensionDtype)
    assert is_extension_array_dtype(dtype)

