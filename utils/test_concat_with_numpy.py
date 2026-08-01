
def test_concat_with_numpy(string_dtype_arguments):
    # common type with a numpy string dtype always preserves the pandas string dtype
    dtype = pd.StringDtype(*string_dtype_arguments)
    assert find_common_type([dtype, np.dtype("U")]) == dtype
    assert find_common_type([np.dtype("U"), dtype]) == dtype
    assert find_common_type([dtype, np.dtype("U10")]) == dtype
    assert find_common_type([np.dtype("U10"), dtype]) == dtype

    # with any other numpy dtype -> object
    assert find_common_type([dtype, np.dtype("S")]) == np.dtype("object")
    assert find_common_type([dtype, np.dtype("int64")]) == np.dtype("object")

    if Version(np.__version__) >= Version("2"):
        assert find_common_type([dtype, np.dtypes.StringDType()]) == dtype
        assert find_common_type([np.dtypes.StringDType(), dtype]) == dtype

