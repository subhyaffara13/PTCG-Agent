
def test_cse_ignore():
    exprs = [exp(y)*(3*y + 3*sqrt(x+1)), exp(y)*(5*y + 5*sqrt(x+1))]
    subst1, red1 = cse(exprs)
    assert any(y in sub.free_symbols for _, sub in subst1), "cse failed to identify any term with y"

    subst2, red2 = cse(exprs, ignore=(y,))  # y is not allowed in substitutions
    assert not any(y in sub.free_symbols for _, sub in subst2), "Sub-expressions containing y must be ignored"
    assert any(sub - sqrt(x + 1) == 0 for _, sub in subst2), "cse failed to identify sqrt(x + 1) as sub-expression"

