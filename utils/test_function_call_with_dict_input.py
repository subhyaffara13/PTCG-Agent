
def test_function_call_with_dict_input(func):
    """Tests with dict input, unpacking via preprocess_pipeline"""
    data = {'a': 1, 'b': 2}
    assert (func(None, data.keys(), data.values()) ==
            "x: ['a', 'b'], y: [1, 2], ls: x, w: xyz, label: None")

