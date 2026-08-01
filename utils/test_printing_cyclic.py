
def test_printing_cyclic():
    p1 = Permutation([0, 2, 1])
    assert repr(p1) == 'Permutation(1, 2)'
    assert str(p1) == '(1 2)'
    p2 = Permutation()
    assert repr(p2) == 'Permutation()'
    assert str(p2) == '()'
    p3 = Permutation([1, 2, 0, 3])
    assert repr(p3) == 'Permutation(3)(0, 1, 2)'

