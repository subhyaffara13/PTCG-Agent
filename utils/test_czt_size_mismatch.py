
def test_CZT_size_mismatch(cls, args):
    # Data size doesn't match function's expected size
    myfunc = cls(*args)
    with pytest.raises(ValueError, match='CZT defined for'):
        myfunc(np.arange(5))

