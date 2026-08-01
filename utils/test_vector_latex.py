
def test_vector_latex():

    a, b, c, d, omega = symbols('a, b, c, d, omega')

    v = (a ** 2 + b / c) * A.x + sqrt(d) * A.y + cos(omega) * A.z

    assert vlatex(v) == (r'(a^{2} + \frac{b}{c})\mathbf{\hat{a}_x} + '
                         r'\sqrt{d}\mathbf{\hat{a}_y} + '
                         r'\cos{\left(\omega \right)}'
                         r'\mathbf{\hat{a}_z}')

    theta, omega, alpha, q = dynamicsymbols('theta, omega, alpha, q')

    v = theta * A.x + omega * omega * A.y + (q * alpha) * A.z

    assert vlatex(v) == (r'\theta\mathbf{\hat{a}_x} + '
                         r'\omega^{2}\mathbf{\hat{a}_y} + '
                         r'\alpha q\mathbf{\hat{a}_z}')

    phi1, phi2, phi3 = dynamicsymbols('phi1, phi2, phi3')
    theta1, theta2, theta3 = symbols('theta1, theta2, theta3')

    v = (sin(theta1) * A.x +
         cos(phi1) * cos(phi2) * A.y +
         cos(theta1 + phi3) * A.z)

    assert vlatex(v) == (r'\sin{\left(\theta_{1} \right)}'
                         r'\mathbf{\hat{a}_x} + \cos{'
                         r'\left(\phi_{1} \right)} \cos{'
                         r'\left(\phi_{2} \right)}\mathbf{\hat{a}_y} + '
                         r'\cos{\left(\theta_{1} + '
                         r'\phi_{3} \right)}\mathbf{\hat{a}_z}')

    N = ReferenceFrame('N')

    a, b, c, d, omega = symbols('a, b, c, d, omega')

    v = (a ** 2 + b / c) * N.x + sqrt(d) * N.y + cos(omega) * N.z

    expected = (r'(a^{2} + \frac{b}{c})\mathbf{\hat{n}_x} + '
                r'\sqrt{d}\mathbf{\hat{n}_y} + '
                r'\cos{\left(\omega \right)}'
                r'\mathbf{\hat{n}_z}')

    assert vlatex(v) == expected

    # Try custom unit vectors.

    N = ReferenceFrame('N', latexs=(r'\hat{i}', r'\hat{j}', r'\hat{k}'))

    v = (a ** 2 + b / c) * N.x + sqrt(d) * N.y + cos(omega) * N.z

    expected = (r'(a^{2} + \frac{b}{c})\hat{i} + '
                r'\sqrt{d}\hat{j} + '
                r'\cos{\left(\omega \right)}\hat{k}')
    assert vlatex(v) == expected

    expected = r'\alpha\mathbf{\hat{n}_x} + \operatorname{asin}{\left(\omega ' \
        r'\right)}\mathbf{\hat{n}_y} -  \beta \dot{\alpha}\mathbf{\hat{n}_z}'
    assert vlatex(ww) == expected

    expected = r'- \mathbf{\hat{n}_x}\otimes \mathbf{\hat{n}_y} - ' \
        r'\mathbf{\hat{n}_x}\otimes \mathbf{\hat{n}_z}'
    assert vlatex(xx) == expected

    expected = r'\mathbf{\hat{n}_x}\otimes \mathbf{\hat{n}_y} + ' \
        r'\mathbf{\hat{n}_x}\otimes \mathbf{\hat{n}_z}'
    assert vlatex(xx2) == expected

