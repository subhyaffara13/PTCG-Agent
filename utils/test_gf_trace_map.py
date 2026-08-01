
def test_gf_trace_map():
    f = ZZ.map([1, 1, 4, 9, 1])
    a = [1, 1, 1]
    c = ZZ.map([1, 0])
    b = gf_pow_mod(c, 11, f, 11, ZZ)

    assert gf_trace_map(a, b, c, 0, f, 11, ZZ) == \
        ([1, 1, 1], [1, 1, 1])
    assert gf_trace_map(a, b, c, 1, f, 11, ZZ) == \
        ([5, 2, 10, 3], [5, 3, 0, 4])
    assert gf_trace_map(a, b, c, 2, f, 11, ZZ) == \
        ([5, 9, 5, 3], [10, 1, 5, 7])
    assert gf_trace_map(a, b, c, 3, f, 11, ZZ) == \
        ([1, 10, 6, 0], [7])
    assert gf_trace_map(a, b, c, 4, f, 11, ZZ) == \
        ([1, 1, 1], [1, 1, 8])
    assert gf_trace_map(a, b, c, 5, f, 11, ZZ) == \
        ([5, 2, 10, 3], [5, 3, 0, 0])
    assert gf_trace_map(a, b, c, 11, f, 11, ZZ) == \
        ([1, 10, 6, 0], [10])

