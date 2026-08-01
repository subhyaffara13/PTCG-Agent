
def test_ufuncify_numpy():
    # This test doesn't use Cython, but if Cython works, then there is a valid
    # C compiler, which is needed.
    has_module('Cython')
    runtest_ufuncify('C99', 'numpy')

