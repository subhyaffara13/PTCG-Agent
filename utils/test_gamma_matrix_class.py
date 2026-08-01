
def test_gamma_matrix_class():
    i, j, k = tensor_indices('i,j,k', LorentzIndex)

    # define another type of TensorHead to see if exprs are correctly handled:
    A = TensorHead('A', [LorentzIndex])

    t = A(k)*G(i)*G(-i)
    ts = simplify_gamma_expression(t)
    assert _is_tensor_eq(ts, Matrix([
        [4, 0, 0, 0],
        [0, 4, 0, 0],
        [0, 0, 4, 0],
        [0, 0, 0, 4]])*A(k))

    t = G(i)*A(k)*G(j)
    ts = simplify_gamma_expression(t)
    assert _is_tensor_eq(ts, A(k)*G(i)*G(j))

    execute_gamma_simplify_tests_for_function(simplify_gamma_expression, D=4)

