
def test_issue_17092():
    x_star = Symbol('x^*')
    assert latex(Derivative(x_star, x_star,2)) == r'\frac{d^{2}}{d \left(x^{*}\right)^{2}} x^{*}'

