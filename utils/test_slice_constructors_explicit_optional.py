
def test_slice_constructors_explicit_optional():
    assert m.make_reversed_slice_size_t_optional() == slice(None, None, -1)
    assert m.make_reversed_slice_size_t_optional_verbose() == slice(None, None, -1)

