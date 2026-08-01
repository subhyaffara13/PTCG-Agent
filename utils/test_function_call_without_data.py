
def test_function_call_without_data(func):
    """Test without data -> no replacements."""
    assert (func(None, "x", "y") ==
            "x: ['x'], y: ['y'], ls: x, w: xyz, label: None")
    assert (func(None, x="x", y="y") ==
            "x: ['x'], y: ['y'], ls: x, w: xyz, label: None")
    assert (func(None, "x", "y", label="") ==
            "x: ['x'], y: ['y'], ls: x, w: xyz, label: ")
    assert (func(None, "x", "y", label="text") ==
            "x: ['x'], y: ['y'], ls: x, w: xyz, label: text")
    assert (func(None, x="x", y="y", label="") ==
            "x: ['x'], y: ['y'], ls: x, w: xyz, label: ")
    assert (func(None, x="x", y="y", label="text") ==
            "x: ['x'], y: ['y'], ls: x, w: xyz, label: text")

