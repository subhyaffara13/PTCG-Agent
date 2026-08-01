
def test_issue_3568():
    beta = Symbol(r'\beta')
    y = beta + x
    assert latex(y) in [r'\beta + x', r'x + \beta']

    beta = Symbol(r'beta')
    y = beta + x
    assert latex(y) in [r'\beta + x', r'x + \beta']

