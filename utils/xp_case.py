
def xp_case(case, xp, batch_A, batch_b, rng=None):
    sparse = issparse(case.A)

    if (not_np := not is_numpy(xp)) and sparse: # TODO: pydata/sparse for sparse tests?
        pytest.skip("sparse tests run only with `np` backend")

    A = xp.asarray(case.A) if not_np else case.A
    b = xp.asarray(case.b) if not_np else case.b

    rng = np.random.default_rng(rng)
    if sparse and (batch_A or batch_b):
        A = A.tocoo()
    if batch_A:
        # apply some random scaling to each system in batch,
        # preserving symmetry, (non-)positive definiteness, Hermiticity
        scaling = np.abs(rng.standard_normal(batch_A + (1, 1)))
        batch_array = xp.asarray(scaling, dtype=A.dtype)
        A = batch_array * A
    if batch_b:
        # apply some random scaling to each RHS in batch
        b = b * xp.asarray(rng.random(batch_b + (1,)), dtype=b.dtype)

    return types.SimpleNamespace(
        name=case.name,
        A=A,
        b=b,
        convergence=case.convergence,
        solver=case.solver,
        casename=case.casename,
    )

