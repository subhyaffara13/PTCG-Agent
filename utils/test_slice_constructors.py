
def test_slice_constructors():
    assert m.make_forward_slice_size_t() == slice(0, -1, 1)
    assert m.make_reversed_slice_object() == slice(None, None, -1)

