
def test_check_case():
    x, X = symbols('x,X')
    raises(CodeGenError, lambda: codegen(('test', x*X), 'f95', 'prefix'))

