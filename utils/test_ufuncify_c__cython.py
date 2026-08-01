
def test_ufuncify_C_Cython():
    has_module('Cython')
    runtest_ufuncify('C99', 'cython')

