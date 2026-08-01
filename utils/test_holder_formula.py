
def test_holder_formula():
    # semiprime
    assert _holder_formula({3, 5}) == 1
    assert _holder_formula({5, 11}) == 2
    # n in A003277 is always 1
    for n in A003277:
        assert _holder_formula(set(factorint(n).keys())) == 1
    # otherwise
    assert _holder_formula({2, 3, 5, 7}) == 12

