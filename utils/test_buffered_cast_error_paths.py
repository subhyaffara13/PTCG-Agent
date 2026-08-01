
def test_buffered_cast_error_paths():
    with pytest.raises(ValueError):
        # The input is cast into an `S3` buffer
        np.nditer((np.array("a", dtype="S1"),), op_dtypes=["i"],
                  casting="unsafe", flags=["buffered"])

    # The `M8[ns]` is cast into the `S3` output
    it = np.nditer((np.array(1, dtype="i"),), op_dtypes=["S1"],
                   op_flags=["writeonly"], casting="unsafe", flags=["buffered"])
    with pytest.raises(ValueError):
        with it:
            buf = next(it)
            buf[...] = "a"  # cannot be converted to int.

