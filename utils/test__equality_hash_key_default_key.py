
def test_EqualityHashKey_default_key():
    EqualityHashDefault = curry(EqualityHashKey, None)
    L1 = [1]
    L2 = [2]
    data1 = [L1, L1, L2, [], [], [1], [2], {}, ()]
    set1 = set(map(EqualityHashDefault, data1))
    set2 = set(map(EqualityHashDefault, [[], [1], [2], {}, ()]))
    assert set1 == set2
    assert len(set1) == 5

    # Test that ``EqualityHashDefault(item)`` is distinct from ``item``
    T0 = ()
    T1 = (1,)
    data2 = list(map(EqualityHashDefault, [T0, T0, T1, T1, (), (1,)]))
    data2.extend([T0, T1, (), (1,)])
    set3 = set(data2)
    assert set3 == {(), (1,), EqualityHashDefault(()),
                        EqualityHashDefault((1,))}
    assert len(set3) == 4
    assert EqualityHashDefault(()) in set3
    assert EqualityHashDefault((1,)) in set3

    # Miscellaneous
    E1 = EqualityHashDefault(L1)
    E2 = EqualityHashDefault(L2)
    assert str(E1) == '=[1]='
    assert repr(E1) == '=[1]='
    assert E1 != E2
    assert not (E1 == E2)
    assert E1 == EqualityHashDefault(L1)
    assert not (E1 != EqualityHashDefault(L1))
    assert E1 != L1
    assert not (E1 == L1)

