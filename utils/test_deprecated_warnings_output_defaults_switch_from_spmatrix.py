
def test_deprecated_warnings_output_defaults_switch_from_spmatrix():
    A = B = np.array([[1, 0], [1, 0]])
    with pytest.deprecated_call(match=".*switching.*sparse array int"):
        construct.kron(A, B)
    with pytest.deprecated_call(match=".*switching.*sparse array int"):
        construct.kronsum(A, B)
    # Note: vstack hstack and bmat do not support all dense input. So no default.
    with pytest.deprecated_call(match=".*switching.*sparse array int"):
        construct.block_diag([A, B])


def test_deprecated_warnings_output_defaults_switch_from_spmatrix():
    A = np.array([[1, 2], [3, 0]])
    with pytest.deprecated_call(match=".*switching.*sparse array int"):
        _extract.tril(A)
    with pytest.deprecated_call(match=".*switching.*sparse array int"):
        _extract.triu(A)

