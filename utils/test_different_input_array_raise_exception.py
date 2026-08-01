
def test_different_input_array_raise_exception(name):
    A = Series(np.random.default_rng(2).standard_normal(50), index=range(50))
    A[:10] = np.nan

    msg = "other must be a DataFrame or Series"
    # exception raised is Exception
    with pytest.raises(ValueError, match=msg):
        getattr(A.ewm(com=20, min_periods=5), name)(
            np.random.default_rng(2).standard_normal(50)
        )

