
def test_more_args_than_pos_parameter():
    @_preprocess_data(replace_names=["x", "y"], label_namer="y")
    def func(ax, x, y, z=1):
        pass

    data = {"a": [1, 2], "b": [8, 9], "w": "NOT"}
    with pytest.raises(TypeError):
        func(None, "a", "b", "z", "z", data=data)

