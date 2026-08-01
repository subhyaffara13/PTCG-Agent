
def test_wrap_twice_f95_f2py():
    has_module('f2py')
    runtest_autowrap_twice('f95', 'f2py')

