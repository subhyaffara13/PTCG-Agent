
def test_issue_6001():
    A = Symbol("A", commutative=False)
    eq = A + A**2
    # it doesn't matter whether it's True or False; they should
    # just all be the same
    assert (
        eq.is_commutative ==
        (eq + 1).is_commutative ==
        (A + 1).is_commutative)

    B = Symbol("B", commutative=False)
    # Although commutative terms could cancel we return True
    # meaning "there are non-commutative symbols; aftersubstitution
    # that definition can change, e.g. (A*B).subs(B,A**-1) -> 1
    assert (sqrt(2)*A).is_commutative is False
    assert (sqrt(2)*A*B).is_commutative is False

