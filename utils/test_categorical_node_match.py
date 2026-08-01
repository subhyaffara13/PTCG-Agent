
def test_categorical_node_match():
    nm = iso.categorical_node_match(["x", "y", "z"], [None] * 3)
    assert nm({"x": 1, "y": 2, "z": 3}, {"x": 1, "y": 2, "z": 3})
    assert not nm({"x": 1, "y": 2, "z": 2}, {"x": 1, "y": 2, "z": 1})

