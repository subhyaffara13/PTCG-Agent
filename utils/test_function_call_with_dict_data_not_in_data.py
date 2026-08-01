
def test_function_call_with_dict_data_not_in_data(func):
    """Test the case that one var is not in data -> half replaces, half kept"""
    data = {"a": [1, 2], "w": "NOT"}
    assert (func(None, "a", "b", data=data) ==
            "x: [1, 2], y: ['b'], ls: x, w: xyz, label: b")
    assert (func(None, x="a", y="b", data=data) ==
            "x: [1, 2], y: ['b'], ls: x, w: xyz, label: b")
    assert (func(None, "a", "b", label="", data=data) ==
            "x: [1, 2], y: ['b'], ls: x, w: xyz, label: ")
    assert (func(None, "a", "b", label="text", data=data) ==
            "x: [1, 2], y: ['b'], ls: x, w: xyz, label: text")
    assert (func(None, x="a", y="b", label="", data=data) ==
            "x: [1, 2], y: ['b'], ls: x, w: xyz, label: ")
    assert (func(None, x="a", y="b", label="text", data=data) ==
            "x: [1, 2], y: ['b'], ls: x, w: xyz, label: text")

