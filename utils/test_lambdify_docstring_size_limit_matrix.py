
def test_lambdify_docstring_size_limit_matrix():

    class MatrixTestCase(LambdifyDocstringTestCase):
        SIGNATURE = 'x, y, z'
        EXPR = (
            'Matrix([[0, x], [x + y + z, x**3 + 3*x**2*y + 3*x**2*z + 3*x*y**2 '
            '+ 6*x*y*z...'
        )
        SRC = (
            'def _lambdifygenerated(x, y, z):\n'
            '    return ImmutableDenseMatrix([[0, x], [x + y + z, x**3 '
            '+ 3*x**2*y + 3*x**2*z + 3*x*y**2 + 6*x*y*z + 3*x*z**2 + y**3 '
            '+ 3*y**2*z + 3*y*z**2 + z**3]])\n'
        )

    x, y, z = symbols('x, y, z')
    expr = Matrix([[S.Zero, x], [x + y + z, ((x + y + z)**3).expand()]])

    test_cases = (
        MatrixTestCase(docstring_limit=None, expected_redacted=False),
        MatrixTestCase(docstring_limit=200, expected_redacted=False),
        MatrixTestCase(docstring_limit=50, expected_redacted=True),
        MatrixTestCase(docstring_limit=0, expected_redacted=True),
        MatrixTestCase(docstring_limit=-1, expected_redacted=True),
    )
    for test_case in test_cases:
        lambdified_expr = lambdify(
            [x, y, z],
            expr,
            'sympy',
            docstring_limit=test_case.docstring_limit,
        )
        assert lambdified_expr.__doc__ == test_case.expected_docstring

