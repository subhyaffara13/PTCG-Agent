
def test_dummy_order_well_defined():
    aa, bb = symbols('a b', above_fermi=True)
    k, l, m = symbols('k l m', below_fermi=True, cls=Dummy)
    c, d = symbols('c d', above_fermi=True, cls=Dummy)
    p, q = symbols('p q', cls=Dummy)

    A = Function('A')
    B = Function('B')
    C = Function('C')
    dums = _get_ordered_dummies

    # We go through all key components in the order of increasing priority,
    # and consider only fully orderable expressions.  Non-orderable expressions
    # are tested elsewhere.

    # pos in first factor determines sort order
    assert dums(A(k, l)*B(l, k)) == [k, l]
    assert dums(A(l, k)*B(l, k)) == [l, k]
    assert dums(A(k, l)*B(k, l)) == [k, l]
    assert dums(A(l, k)*B(k, l)) == [l, k]

    # factors involving the index
    assert dums(A(k, l)*B(l, m)*C(k, m)) == [l, k, m]
    assert dums(A(k, l)*B(l, m)*C(m, k)) == [l, k, m]
    assert dums(A(l, k)*B(l, m)*C(k, m)) == [l, k, m]
    assert dums(A(l, k)*B(l, m)*C(m, k)) == [l, k, m]
    assert dums(A(k, l)*B(m, l)*C(k, m)) == [l, k, m]
    assert dums(A(k, l)*B(m, l)*C(m, k)) == [l, k, m]
    assert dums(A(l, k)*B(m, l)*C(k, m)) == [l, k, m]
    assert dums(A(l, k)*B(m, l)*C(m, k)) == [l, k, m]

    # same, but with factor order determined by non-dummies
    assert dums(A(k, aa, l)*A(l, bb, m)*A(bb, k, m)) == [l, k, m]
    assert dums(A(k, aa, l)*A(l, bb, m)*A(bb, m, k)) == [l, k, m]
    assert dums(A(k, aa, l)*A(m, bb, l)*A(bb, k, m)) == [l, k, m]
    assert dums(A(k, aa, l)*A(m, bb, l)*A(bb, m, k)) == [l, k, m]
    assert dums(A(l, aa, k)*A(l, bb, m)*A(bb, k, m)) == [l, k, m]
    assert dums(A(l, aa, k)*A(l, bb, m)*A(bb, m, k)) == [l, k, m]
    assert dums(A(l, aa, k)*A(m, bb, l)*A(bb, k, m)) == [l, k, m]
    assert dums(A(l, aa, k)*A(m, bb, l)*A(bb, m, k)) == [l, k, m]

    # index range
    assert dums(A(p, c, k)*B(p, c, k)) == [k, c, p]
    assert dums(A(p, k, c)*B(p, c, k)) == [k, c, p]
    assert dums(A(c, k, p)*B(p, c, k)) == [k, c, p]
    assert dums(A(c, p, k)*B(p, c, k)) == [k, c, p]
    assert dums(A(k, c, p)*B(p, c, k)) == [k, c, p]
    assert dums(A(k, p, c)*B(p, c, k)) == [k, c, p]
    assert dums(B(p, c, k)*A(p, c, k)) == [k, c, p]
    assert dums(B(p, k, c)*A(p, c, k)) == [k, c, p]
    assert dums(B(c, k, p)*A(p, c, k)) == [k, c, p]
    assert dums(B(c, p, k)*A(p, c, k)) == [k, c, p]
    assert dums(B(k, c, p)*A(p, c, k)) == [k, c, p]
    assert dums(B(k, p, c)*A(p, c, k)) == [k, c, p]

