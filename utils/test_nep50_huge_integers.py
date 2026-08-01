
def test_nep50_huge_integers(ufunc):
    # Very large integers are complicated, because they go to uint64 or
    # object dtype.  This tests covers a few possible paths.
    with pytest.raises(OverflowError):
        ufunc(np.int64(0), 2**63)  # 2**63 too large for int64

    with pytest.raises(OverflowError):
        ufunc(np.uint64(0), 2**64)  # 2**64 cannot be represented by uint64

    # However, 2**63 can be represented by the uint64 (and that is used):
    res = ufunc(np.uint64(1), 2**63)

    assert res.dtype == np.uint64
    assert res == ufunc(1, 2**63, dtype=object)

    # The following paths fail to warn correctly about the change:
    with pytest.raises(OverflowError):
        ufunc(np.int64(1), 2**63)  # np.array(2**63) would go to uint

    with pytest.raises(OverflowError):
        ufunc(np.int64(1), 2**100)  # np.array(2**100) would go to object

    # This would go to object and thus a Python float, not a NumPy one:
    res = ufunc(1.0, 2**100)
    assert isinstance(res, np.float64)

