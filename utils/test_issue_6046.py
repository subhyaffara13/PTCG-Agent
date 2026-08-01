
def test_issue_6046():
    assert str(S("Q & C", locals=_clash1)) == 'C & Q'
    assert str(S('pi(x)', locals=_clash2)) == 'pi(x)'
    locals = {}
    exec("from sympy.abc import Q, C", locals)
    assert str(S('C&Q', locals)) == 'C & Q'
    # clash can act as Symbol or Function
    assert str(S('pi(C, Q)', locals=_clash)) == 'pi(C, Q)'
    assert len(S('pi + x', locals=_clash2).free_symbols) == 2
    # but not both
    raises(TypeError, lambda: S('pi + pi(x)', locals=_clash2))
    assert all(set(i.values()) == {null} for i in (
        _clash, _clash1, _clash2))

