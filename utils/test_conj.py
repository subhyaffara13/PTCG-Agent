
def test_conj():
    assert fp.conj(4) == 4
    assert fp.conj(3+4j) == 3-4j
    assert fp.fdot([1,2],[3,2+1j], conjugate=True) == 7-2j

