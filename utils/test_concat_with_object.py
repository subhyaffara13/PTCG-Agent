
def test_concat_with_object(string_dtype_arguments):
    # _get_common_dtype cannot inspect values, so object dtype with strings still
    # results in object dtype
    result = pd.concat(
        [
            pd.Series(["a", "b", None], dtype=pd.StringDtype(*string_dtype_arguments)),
            pd.Series(["a", "b", None], dtype=object),
        ]
    )
    assert result.dtype == np.dtype("object")

