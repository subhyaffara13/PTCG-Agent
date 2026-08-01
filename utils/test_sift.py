
def test_sift():
    assert sift(list(range(5)), lambda _: _ % 2) == {1: [1, 3], 0: [0, 2, 4]}
    assert sift([x, y], lambda _: _.has(x)) == {False: [y], True: [x]}
    assert sift([S.One], lambda _: _.has(x)) == {False: [1]}
    assert sift([0, 1, 2, 3], lambda x: x % 2, binary=True) == (
        [1, 3], [0, 2])
    assert sift([0, 1, 2, 3], lambda x: x % 3 == 1, binary=True) == (
        [1], [0, 2, 3])
    raises(ValueError, lambda:
        sift([0, 1, 2, 3], lambda x: x % 3, binary=True))

