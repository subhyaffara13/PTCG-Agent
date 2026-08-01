
def test_hilbert_space():
    hs = HilbertSpace()
    assert isinstance(hs, HilbertSpace)
    assert sstr(hs) == 'H'
    assert srepr(hs) == 'HilbertSpace()'

