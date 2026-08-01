
def test_signed_permutations():
    ans = [(0, 1, 1), (0, -1, 1), (0, 1, -1), (0, -1, -1),
    (1, 0, 1), (-1, 0, 1), (1, 0, -1), (-1, 0, -1),
    (1, 1, 0), (-1, 1, 0), (1, -1, 0), (-1, -1, 0)]
    assert list(signed_permutations((0, 1, 1))) == ans
    assert list(signed_permutations((1, 0, 1))) == ans
    assert list(signed_permutations((1, 1, 0))) == ans

