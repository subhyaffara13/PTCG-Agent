
def test_make_c_f_array():
    assert m.make_c_array().flags.c_contiguous
    assert not m.make_c_array().flags.f_contiguous
    assert m.make_f_array().flags.f_contiguous
    assert not m.make_f_array().flags.c_contiguous

