
def test_index_name_with_dict_like_raising():
    # GH#20421
    ix = pd.Index([1, 2])
    msg = "Can only pass dict-like as `names` for MultiIndex."
    with pytest.raises(TypeError, match=msg):
        ix.set_names({"x": "z"})

