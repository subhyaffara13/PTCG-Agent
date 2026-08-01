
def test_no_arith_subs_on_floats():
    assert (x + 3).subs(x + 3, a) == a
    assert (x + 3).subs(x + 2, a) == a + 1

    assert (x + y + 3).subs(x + 3, a) == a + y
    assert (x + y + 3).subs(x + 2, a) == a + y + 1

    assert (x + 3.0).subs(x + 3.0, a) == a
    assert (x + 3.0).subs(x + 2.0, a) == x + 3.0

    assert (x + y + 3.0).subs(x + 3.0, a) == a + y
    assert (x + y + 3.0).subs(x + 2.0, a) == x + y + 3.0

