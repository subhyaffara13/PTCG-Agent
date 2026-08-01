
def test_replace_categorical_ea_dtype():
    # GH49404
    cat = Categorical(pd.array(["a", "b", "c"], dtype="string"))
    result = pd.Series(cat).replace(["a", "b"], ["c", "c"])._values
    expected = Categorical(
        pd.array(["c"] * 3, dtype="string"),
        categories=pd.array(["a", "b", "c"], dtype="string"),
    )
    tm.assert_categorical_equal(result, expected)

