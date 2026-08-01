
def test_result_type_integers_and_unitless_timedelta64():
    # Regression test for gh-20077.  The following call of `result_type`
    # would cause a seg. fault.
    with pytest.warns(
        DeprecationWarning,
        match="The 'generic' unit for NumPy timedelta is deprecated",
    ):
        td = np.timedelta64(4)
        result = np.result_type(0, td)
        assert_dtype_equal(result, td.dtype)

