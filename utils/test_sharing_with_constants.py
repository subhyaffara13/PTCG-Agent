
def test_sharing_with_constants(backend: BackendType) -> None:
    inputs = "ij,jk,kl"
    outputs = "ijkl"
    equations = [f"{inputs}->{output}" for output in outputs]
    shapes = (2, 3), (3, 4), (4, 5)
    constants = {0, 2}
    ops = [np.random.rand(*shp) if i in constants else shp for i, shp in enumerate(shapes)]
    var = np.random.rand(*shapes[1])

    expected = [contract_expression(eq, *shapes)(ops[0], var, ops[2]) for eq in equations]

    with shared_intermediates():
        actual = [contract_expression(eq, *ops, constants=constants)(var) for eq in equations]

    for dim, expected_dim, actual_dim in zip(outputs, expected, actual):
        assert np.allclose(expected_dim, actual_dim), f"error at {dim}"

