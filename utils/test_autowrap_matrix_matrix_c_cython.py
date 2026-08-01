
def test_autowrap_matrix_matrix_C_cython():
    has_module('Cython')
    runtest_autowrap_matrix_matrix('C99', 'cython')

