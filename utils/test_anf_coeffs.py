
def test_anf_coeffs():
    assert anf_coeffs([1, 0]) == [1, 1]
    assert anf_coeffs([0, 0, 0, 1]) == [0, 0, 0, 1]
    assert anf_coeffs([0, 1, 1, 1]) == [0, 1, 1, 1]
    assert anf_coeffs([1, 1, 1, 0]) == [1, 0, 0, 1]
    assert anf_coeffs([1, 0, 0, 0]) == [1, 1, 1, 1]
    assert anf_coeffs([1, 0, 0, 1]) == [1, 1, 1, 0]
    assert anf_coeffs([1, 1, 0, 1]) == [1, 0, 1, 1]

