
def test_issue_21721():
    a = Symbol('a', real=True)
    I = integrate(1/(pi*(1 + (x - a)**2)), x)
    assert I.limit(x, oo) == S.Half


def test_issue_21721():
    a = Symbol('a')
    assert integrate(1/(pi*(1+(x-a)**2)),(x,-oo,oo)).expand() == \
    -Heaviside(im(a) - 1, 0) + Heaviside(im(a) + 1, 0)

