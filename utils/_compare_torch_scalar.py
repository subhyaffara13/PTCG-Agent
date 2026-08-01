
def _compare_torch_scalar(variables, expr, rng=lambda: random.uniform(-5, 5)):
    f = lambdify(variables, expr, 'torch')
    rvs = [rng() for v in variables]
    t_rvs = [torch.tensor(i, dtype=torch.float64) for i in rvs]
    r = f(*t_rvs)
    if isinstance(r, torch.Tensor):
        r = r.item()
    e = expr.subs(dict(zip(variables, rvs))).doit()
    assert abs(r - e) < 1e-6

