
def test_is_numeric_v_string_like():
    assert not com.is_numeric_v_string_like(np.array([1]), 1)
    assert not com.is_numeric_v_string_like(np.array([1]), np.array([2]))
    assert not com.is_numeric_v_string_like(np.array(["foo"]), np.array(["foo"]))

    assert com.is_numeric_v_string_like(np.array([1]), "foo")
    assert com.is_numeric_v_string_like(np.array([1, 2]), np.array(["foo"]))
    assert com.is_numeric_v_string_like(np.array(["foo"]), np.array([1, 2]))

