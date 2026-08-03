from typing import Union

def test_SetKind_evaluate_False():
    U = lambda *args: Union(*args, evaluate=False)
    assert U({1}, EmptySet).kind is SetKind(NumberKind)
    assert U(Interval(1, 2), EmptySet).kind is SetKind(NumberKind)
    assert U({1}, S.UniversalSet).kind is SetKind(UndefinedKind)
    assert U(Interval(1, 2), Interval(4, 5),
            FiniteSet(1)).kind is SetKind(NumberKind)
    I = lambda *args: Intersection(*args, evaluate=False)
    assert I({1}, S.UniversalSet).kind is SetKind(NumberKind)
    assert I({1}, EmptySet).kind is SetKind()
    C = lambda *args: Complement(*args, evaluate=False)
    assert C(S.UniversalSet, {1, 2, 4, 5}).kind is SetKind(UndefinedKind)
    assert C({1, 2, 3, 4, 5}, EmptySet).kind is SetKind(NumberKind)
    assert C(EmptySet, {1, 2, 3, 4, 5}).kind is SetKind()

