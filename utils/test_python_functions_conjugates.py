
def test_python_functions_conjugates():
    a, b = map(Symbol, 'ab')
    assert python( conjugate(a + b*I) ) == '_     _\na - I*b'
    assert python( conjugate(exp(a + b*I)) ) == ' _     _\n a - I*b\ne       '

