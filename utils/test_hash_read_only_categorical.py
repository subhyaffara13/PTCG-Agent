
def test_hash_read_only_categorical():
    # GH#58481
    idx = pd.Index(pd.Index(["a", "b", "c"], dtype="object").values)
    cat = pd.CategoricalDtype(idx)
    arr = pd.Series(["a", "b"], dtype=cat).values
    assert hash(arr.dtype) == hash(arr.dtype)

