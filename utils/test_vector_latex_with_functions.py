
def test_vector_latex_with_functions():

    N = ReferenceFrame('N')

    omega, alpha = dynamicsymbols('omega, alpha')

    v = omega.diff() * N.x

    assert vlatex(v) == r'\dot{\omega}\mathbf{\hat{n}_x}'

    v = omega.diff() ** alpha * N.x

    assert vlatex(v) == (r'\dot{\omega}^{\alpha}'
                          r'\mathbf{\hat{n}_x}')

