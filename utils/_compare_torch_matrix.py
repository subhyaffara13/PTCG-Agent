
def _compare_torch_matrix(variables, expr):
    f = lambdify(variables, expr, 'torch')

    random_matrices = [randMatrix(i.shape[0], i.shape[1]) for i in variables]
    random_variables = [torch.tensor(i.tolist(), dtype=torch.float64) for i in random_matrices]
    r = f(*random_variables)
    e = expr.subs(dict(zip(variables, random_matrices))).doit()

    if isinstance(e, _CodegenArrayAbstract):
        e = e.doit()

    if hasattr(e, 'is_number') and e.is_number:
        if isinstance(r, torch.Tensor) and r.dim() == 0:
            r = r.item()
            e = float(e)
            assert abs(r - e) < 1e-6
            return

    if e.is_Matrix or isinstance(e, NDimArray):
        e = torch.tensor(e.tolist(), dtype=torch.float64)
        assert torch.allclose(r, e, atol=1e-6)
    else:
        raise TypeError(f"Cannot compare {type(r)} with {type(e)}")

