
def test_issue_10489():
    latexSymbolWithBrace = r'C_{x_{0}}'
    s = Symbol(latexSymbolWithBrace)
    assert latex(s) == latexSymbolWithBrace
    assert latex(cos(s)) == r'\cos{\left(C_{x_{0}} \right)}'

