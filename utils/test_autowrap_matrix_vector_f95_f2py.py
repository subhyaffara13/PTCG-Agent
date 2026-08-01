
def test_autowrap_matrix_vector_f95_f2py():
    has_module('f2py')
    runtest_autowrap_matrix_vector('f95', 'f2py')

