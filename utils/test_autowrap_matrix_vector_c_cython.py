
def test_autowrap_matrix_vector_C_cython():
    has_module('Cython')
    runtest_autowrap_matrix_vector('C99', 'cython')

