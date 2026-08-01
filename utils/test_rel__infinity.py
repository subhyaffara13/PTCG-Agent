
def test_rel_Infinity():
    # NOTE: All of these are actually handled by sympy.core.Number, and do
    # not create Relational objects.
    assert (oo > oo) is S.false
    assert (oo > -oo) is S.true
    assert (oo > 1) is S.true
    assert (oo < oo) is S.false
    assert (oo < -oo) is S.false
    assert (oo < 1) is S.false
    assert (oo >= oo) is S.true
    assert (oo >= -oo) is S.true
    assert (oo >= 1) is S.true
    assert (oo <= oo) is S.true
    assert (oo <= -oo) is S.false
    assert (oo <= 1) is S.false
    assert (-oo > oo) is S.false
    assert (-oo > -oo) is S.false
    assert (-oo > 1) is S.false
    assert (-oo < oo) is S.true
    assert (-oo < -oo) is S.false
    assert (-oo < 1) is S.true
    assert (-oo >= oo) is S.false
    assert (-oo >= -oo) is S.true
    assert (-oo >= 1) is S.false
    assert (-oo <= oo) is S.true
    assert (-oo <= -oo) is S.true
    assert (-oo <= 1) is S.true

