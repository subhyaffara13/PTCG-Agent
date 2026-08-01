
def test_Cycle():
    # FIXME: sT fails because Cycle is not immutable and calling srepr(Cycle(1, 2))
    # adds keys to the Cycle dict (GH-17661)
    #import_stmt = "from sympy.combinatorics import Cycle"
    #sT(Cycle(1, 2), "Cycle(1, 2)", import_stmt)
    assert srepr(Cycle(1, 2)) == "Cycle(1, 2)"


def test_Cycle():
    assert str(Cycle()) == '()'
    assert Cycle(Cycle(1,2)) == Cycle(1, 2)
    assert Cycle(1,2).copy() == Cycle(1,2)
    assert list(Cycle(1, 3, 2)) == [0, 3, 1, 2]
    assert Cycle(1, 2)(2, 3) == Cycle(1, 3, 2)
    assert Cycle(1, 2)(2, 3)(4, 5) == Cycle(1, 3, 2)(4, 5)
    assert Permutation(Cycle(1, 2)(2, 1, 0, 3)).cyclic_form, Cycle(0, 2, 1)
    raises(ValueError, lambda: Cycle().list())
    assert Cycle(1, 2).list() == [0, 2, 1]
    assert Cycle(1, 2).list(4) == [0, 2, 1, 3]
    assert Cycle(3).list(2) == [0, 1]
    assert Cycle(3).list(6) == [0, 1, 2, 3, 4, 5]
    assert Permutation(Cycle(1, 2), size=4) == \
        Permutation([0, 2, 1, 3])
    assert str(Cycle(1, 2)(4, 5)) == '(1 2)(4 5)'
    assert str(Cycle(1, 2)) == '(1 2)'
    assert Cycle(Permutation(list(range(3)))) == Cycle()
    assert Cycle(1, 2).list() == [0, 2, 1]
    assert Cycle(1, 2).list(4) == [0, 2, 1, 3]
    assert Cycle().size == 0
    raises(ValueError, lambda: Cycle((1, 2)))
    raises(ValueError, lambda: Cycle(1, 2, 1))
    raises(TypeError, lambda: Cycle(1, 2)*{})
    raises(ValueError, lambda: Cycle(4)[a])
    raises(ValueError, lambda: Cycle(2, -4, 3))

    # check round-trip
    p = Permutation([[1, 2], [4, 3]], size=5)
    assert Permutation(Cycle(p)) == p

