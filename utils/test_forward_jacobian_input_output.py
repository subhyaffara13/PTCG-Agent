
def test_forward_jacobian_input_output():
    x, y, z = symbols('x y z')
    expr = Matrix([
        x * y + y * z + x * y * z,
        x ** 2 + y ** 2 + z ** 2,
        x * y + x * z + y * z
    ])
    wrt = Matrix([x, y, z])

    replacements, reduced_expr = cse(expr)

    # Test _forward_jacobian_core
    replacements_core, jacobian_core, precomputed_fs_core = _forward_jacobian_cse(replacements, reduced_expr, wrt)
    assert isinstance(replacements_core, type(replacements)), "Replacements should be a list"
    assert isinstance(jacobian_core, type(reduced_expr)), "Jacobian should be a list"
    assert isinstance(precomputed_fs_core, list), "Precomputed free symbols should be a list"
    assert len(replacements_core) == len(replacements), "Length of replacements does not match"
    assert len(jacobian_core) == 1, "Jacobian should have one element"
    assert len(precomputed_fs_core) == len(replacements), "Length of precomputed free symbols does not match"

    # Test _forward_jacobian_norm_in_dag_out
    replacements_norm, jacobian_norm, precomputed_fs_norm = _forward_jacobian_norm_in_cse_out(expr, wrt)
    assert isinstance(replacements_norm, type(replacements)), "Replacements should be a list"
    assert isinstance(jacobian_norm, type(reduced_expr)), "Jacobian should be a list"
    assert isinstance(precomputed_fs_norm, list), "Precomputed free symbols should be a list"
    assert len(replacements_norm) == len(replacements), "Length of replacements does not match"
    assert len(jacobian_norm) == 1, "Jacobian should have one element"
    assert len(precomputed_fs_norm) == len(replacements), "Length of precomputed free symbols does not match"

