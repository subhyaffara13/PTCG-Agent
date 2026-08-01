
def test_latex_Poly_order():
    assert latex(Poly([a, 1, b, 2, c, 3], x)) == \
        r'\operatorname{Poly}{\left( a x^{5} + x^{4} + b x^{3} + 2 x^{2} + c'\
        r' x + 3, x, domain=\mathbb{Z}\left[a, b, c\right] \right)}'
    assert latex(Poly([a, 1, b+c, 2, 3], x)) == \
        r'\operatorname{Poly}{\left( a x^{4} + x^{3} + \left(b + c\right) '\
        r'x^{2} + 2 x + 3, x, domain=\mathbb{Z}\left[a, b, c\right] \right)}'
    assert latex(Poly(a*x**3 + x**2*y - x*y - c*y**3 - b*x*y**2 + y - a*x + b,
                      (x, y))) == \
        r'\operatorname{Poly}{\left( a x^{3} + x^{2}y -  b xy^{2} - xy -  '\
        r'a x -  c y^{3} + y + b, x, y, domain=\mathbb{Z}\left[a, b, c\right] \right)}'

