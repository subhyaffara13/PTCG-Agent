
def test_lambdify_docstring_size_limit_simple_symbol():

    class SimpleSymbolTestCase(LambdifyDocstringTestCase):
        SIGNATURE = 'x'
        EXPR = 'x'
        SRC = (
            'def _lambdifygenerated(x):\n'
            '    return x\n'
        )

    x = symbols('x')

    test_cases = (
        SimpleSymbolTestCase(docstring_limit=None, expected_redacted=False),
        SimpleSymbolTestCase(docstring_limit=100, expected_redacted=False),
        SimpleSymbolTestCase(docstring_limit=1, expected_redacted=False),
        SimpleSymbolTestCase(docstring_limit=0, expected_redacted=True),
        SimpleSymbolTestCase(docstring_limit=-1, expected_redacted=True),
    )
    for test_case in test_cases:
        lambdified_expr = lambdify(
            [x],
            x,
            'sympy',
            docstring_limit=test_case.docstring_limit,
        )
        assert lambdified_expr.__doc__ == test_case.expected_docstring

