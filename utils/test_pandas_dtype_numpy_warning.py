
def test_pandas_dtype_numpy_warning():
    # GH#51523
    if Version(np.__version__) < Version("2.3.0.dev0"):
        ctx = tm.assert_produces_warning(
            DeprecationWarning,
            check_stacklevel=False,
            match=(
                "Converting `np.integer` or `np.signedinteger` to a dtype is deprecated"
            ),
        )
    else:
        ctx = tm.external_error_raised(TypeError)

    with ctx:
        pandas_dtype(np.integer)

