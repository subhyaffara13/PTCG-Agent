
def test_matrix_element_sets_determinant_trace():
    assert ask(Q.integer(Determinant(X)), Q.integer_elements(X))
    assert ask(Q.integer(Trace(X)), Q.integer_elements(X))

