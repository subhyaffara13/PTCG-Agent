
def test_dataframe_multiple_numpy_dtypes():
    df = DataFrame({"a": [1, 2, 3], "b": 1.5})
    arr = np.asarray(df)
    assert not np.shares_memory(arr, get_array(df, "a"))
    assert arr.flags.writeable is True

    if np_version_gt2:
        # copy=False semantics are only supported in NumPy>=2.

        with pytest.raises(ValueError, match="Unable to avoid copy while creating"):
            arr = np.array(df, copy=False)

    arr = np.array(df, copy=True)
    assert arr.flags.writeable is True

