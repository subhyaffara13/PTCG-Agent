
def test_constructor_nan_like(na):
    expected = pd.arrays.StringArray(np.array(["a", pd.NA]), dtype=pd.StringDtype())
    result = pd.arrays.StringArray(
        np.array(["a", na], dtype="object"), dtype=pd.StringDtype()
    )
    tm.assert_extension_array_equal(result, expected)

