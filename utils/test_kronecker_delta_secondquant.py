
def test_kronecker_delta_secondquant():
    """secondquant-specific methods"""
    D = KroneckerDelta
    i, j, v, w = symbols('i j v w', below_fermi=True, cls=Dummy)
    a, b, t, u = symbols('a b t u', above_fermi=True, cls=Dummy)
    p, q, r, s = symbols('p q r s', cls=Dummy)

    assert D(i, a) == 0
    assert D(i, t) == 0

    assert D(i, j).is_above_fermi is False
    assert D(a, b).is_above_fermi is True
    assert D(p, q).is_above_fermi is True
    assert D(i, q).is_above_fermi is False
    assert D(q, i).is_above_fermi is False
    assert D(q, v).is_above_fermi is False
    assert D(a, q).is_above_fermi is True

    assert D(i, j).is_below_fermi is True
    assert D(a, b).is_below_fermi is False
    assert D(p, q).is_below_fermi is True
    assert D(p, j).is_below_fermi is True
    assert D(q, b).is_below_fermi is False

    assert D(i, j).is_only_above_fermi is False
    assert D(a, b).is_only_above_fermi is True
    assert D(p, q).is_only_above_fermi is False
    assert D(i, q).is_only_above_fermi is False
    assert D(q, i).is_only_above_fermi is False
    assert D(a, q).is_only_above_fermi is True

    assert D(i, j).is_only_below_fermi is True
    assert D(a, b).is_only_below_fermi is False
    assert D(p, q).is_only_below_fermi is False
    assert D(p, j).is_only_below_fermi is True
    assert D(q, b).is_only_below_fermi is False

    assert not D(i, q).indices_contain_equal_information
    assert not D(a, q).indices_contain_equal_information
    assert D(p, q).indices_contain_equal_information
    assert D(a, b).indices_contain_equal_information
    assert D(i, j).indices_contain_equal_information

    assert D(q, b).preferred_index == b
    assert D(q, b).killable_index == q
    assert D(q, t).preferred_index == t
    assert D(q, t).killable_index == q
    assert D(q, i).preferred_index == i
    assert D(q, i).killable_index == q
    assert D(q, v).preferred_index == v
    assert D(q, v).killable_index == q
    assert D(q, p).preferred_index == p
    assert D(q, p).killable_index == q

    EV = evaluate_deltas
    assert EV(D(a, q)*F(q)) == F(a)
    assert EV(D(i, q)*F(q)) == F(i)
    assert EV(D(a, q)*F(a)) == D(a, q)*F(a)
    assert EV(D(i, q)*F(i)) == D(i, q)*F(i)
    assert EV(D(a, b)*F(a)) == F(b)
    assert EV(D(a, b)*F(b)) == F(a)
    assert EV(D(i, j)*F(i)) == F(j)
    assert EV(D(i, j)*F(j)) == F(i)
    assert EV(D(p, q)*F(q)) == F(p)
    assert EV(D(p, q)*F(p)) == F(q)
    assert EV(D(p, j)*D(p, i)*F(i)) == F(j)
    assert EV(D(p, j)*D(p, i)*F(j)) == F(i)
    assert EV(D(p, q)*D(p, i))*F(i) == D(q, i)*F(i)

