
def test_recursive_casting():
    """Tests that stl casters preserve lvalue/rvalue context for container values"""
    assert m.cast_rv_vector() == ["rvalue", "rvalue"]
    assert m.cast_lv_vector() == ["lvalue", "lvalue"]
    assert m.cast_rv_array() == ["rvalue", "rvalue", "rvalue"]
    assert m.cast_lv_array() == ["lvalue", "lvalue"]
    assert m.cast_rv_map() == {"a": "rvalue"}
    assert m.cast_lv_map() == {"a": "lvalue", "b": "lvalue"}
    assert m.cast_rv_nested() == [[[{"b": "rvalue", "c": "rvalue"}], [{"a": "rvalue"}]]]
    assert m.cast_lv_nested() == {
        "a": [[["lvalue", "lvalue"]], [["lvalue", "lvalue"]]],
        "b": [[["lvalue", "lvalue"], ["lvalue", "lvalue"]]],
    }

    # Issue #853 test case:
    z = m.cast_unique_ptr_vector()
    assert z[0].value == 7
    assert z[1].value == 42

