
def test_io_matrix_type():
    x, y, z = symbols('x y z')
    expr = ImmutableDenseMatrix([
        x * y + y * z + x * y * z,
        x ** 2 + y ** 2 + z ** 2,
        x * y + x * z + y * z
    ])
    wrt = ImmutableDenseMatrix([x, y, z])

    replacements, reduced_expr = cse(expr)

    # Test _forward_jacobian_core
    replacements_core, jacobian_core, precomputed_fs_core = _forward_jacobian_cse(replacements, reduced_expr, wrt)
    assert isinstance(jacobian_core[0], type(reduced_expr[0])), "Jacobian should be a Matrix of the same type as the input"

    # Test _forward_jacobian_norm_in_dag_out
    replacements_norm, jacobian_norm, precomputed_fs_norm = _forward_jacobian_norm_in_cse_out(
        expr, wrt)
    assert isinstance(jacobian_norm[0], type(reduced_expr[0])), "Jacobian should be a Matrix of the same type as the input"

    # Test _forward_jacobian
    jacobian = _forward_jacobian(expr, wrt)
    assert isinstance(jacobian, type(expr)), "Jacobian should be a Matrix of the same type as the input"

