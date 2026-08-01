
def test_wrap_twice_c_cython():
    has_module('Cython')
    runtest_autowrap_twice('C', 'cython')

