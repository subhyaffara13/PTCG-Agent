from typing import Set

def test_torch_with_constants(constants: Set[int]) -> None:
    torch = pytest.importorskip("torch")

    eq = "ij,jk,kl->li"
    shapes = (2, 3), (3, 4), (4, 5)
    (non_const,) = {0, 1, 2} - constants
    ops = [torch.rand(*shp) if i in constants else shp for i, shp in enumerate(shapes)]
    var = torch.rand(*shapes[non_const])
    res_exp = contract(eq, *(ops[i] if i in constants else var for i in range(3)), backend="torch")

    expr = contract_expression(eq, *ops, constants=constants)

    # check torch
    res_got = expr(var, backend="torch")
    assert all(array is None or infer_backend(array) == "torch" for array in expr._evaluated_constants["torch"])
    torch.testing.assert_close(res_exp, res_got)

    # check can call with numpy still
    res_got2 = expr(var, backend="torch")
    torch.testing.assert_close(res_exp, res_got2)

    # check torch call returns torch still
    res_got3 = expr(backends.to_torch(var))
    assert isinstance(res_got3, torch.Tensor)
    torch.testing.assert_close(res_exp, res_got3)

