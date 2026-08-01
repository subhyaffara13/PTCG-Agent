
def test_type_selection():
    assert m.selective_func(np.array([1], dtype=np.int32)) == "Int branch taken."
    assert m.selective_func(np.array([1.0], dtype=np.float32)) == "Float branch taken."
    assert (
        m.selective_func(np.array([1.0j], dtype=np.complex64))
        == "Complex float branch taken."
    )

