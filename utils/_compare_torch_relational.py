import random

def _compare_torch_relational(variables, expr, rng=lambda: random.randint(0, 10)):
    f = lambdify(variables, expr, 'torch')
    rvs = [rng() for v in variables]
    t_rvs = [torch.tensor(i, dtype=torch.float64) for i in rvs]
    r = f(*t_rvs)
    e = bool(expr.subs(dict(zip(variables, rvs))).doit())
    assert r.item() == e

