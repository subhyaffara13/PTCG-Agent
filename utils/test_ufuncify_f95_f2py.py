
def test_ufuncify_f95_f2py():
    has_module('f2py')
    runtest_ufuncify('f95', 'f2py')

