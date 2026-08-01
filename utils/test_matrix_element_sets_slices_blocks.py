
def test_matrix_element_sets_slices_blocks():
    X = MatrixSymbol('X', 4, 4)
    assert ask(Q.integer_elements(X[:, 3]), Q.integer_elements(X))
    assert ask(Q.integer_elements(BlockMatrix([[X], [X]])),
                        Q.integer_elements(X))

