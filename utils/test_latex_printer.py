
def test_latex_printer():
    r = Function('r')('t')
    assert VectorLatexPrinter().doprint(r ** 2) == "r^{2}"
    r2 = Function('r^2')('t')
    assert VectorLatexPrinter().doprint(r2.diff()) == r'\dot{r^{2}}'
    ra = Function('r__a')('t')
    assert VectorLatexPrinter().doprint(ra.diff().diff()) == r'\ddot{r^{a}}'

