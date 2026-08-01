
def test_replace_categorical_ea_dtype_different_cats_raises():
    # GH49404
    cat = Categorical(pd.array(["a", "b"], dtype="string"))
    with pytest.raises(
        TypeError, match="Cannot setitem on a Categorical with a new category"
    ):
        pd.Series(cat).replace(["a", "b"], ["c", pd.NA])

