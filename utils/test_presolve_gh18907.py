
def test_presolve_gh18907():
    from scipy.optimize import milp
    import numpy as np
    inf = np.inf

    # set up problem
    c = np.array([-0.85850509, -0.82892676, -0.80026454, -0.63015535, -0.5099006,
                  -0.50077193, -0.4894404, -0.47285865,  -0.39867774, -0.38069646,
                  -0.36733012, -0.36733012, -0.35820411, -0.31576141, -0.20626091,
                  -0.12466144, -0.10679516, -0.1061887, -0.1061887, -0.1061887,
                  -0., -0., -0., -0., 0., 0., 0., 0.])

    A = np.array([[1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
                   1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 0., 0., 0., 0.],
                  [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
                   1., 0., 0., 0., 0., 0., 1., 0., 0., 0., -25., -0., -0., -0.],
                  [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
                   -1., 0., 0., 0., 0., 0., -1., 0., 0., 0., 2., 0., 0., 0.],
                  [0., 0., 0., 0., 1., 1., 1., 1., 0., 1., 0., 0., 0., 0., 0.,
                   0., 0., 0., 0., 0., 0., 0., 0., 0., -0., -25., -0., -0.],
                  [0., 0., 0., 0., -1., -1., -1., -1., 0., -1., 0., 0., 0.,
                   0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 2., 0., 0.],
                  [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
                   0., 0., 1., 1., 1., 0., 0., 0., 0., -0., -0., -25., -0.],
                  [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
                   0., 0., -1., -1., -1., 0., 0., 0., 0., 0., 0., 2., 0.],
                  [1., 1., 1., 1., 0., 0., 0., 0., 1., 0., 1., 1., 1., 1., 0.,
                   1., 1., 0., 0., 0., 0., 1., 1., 1., -0., -0., -0., -25.],
                  [-1., -1., -1., -1., 0., 0., 0., 0., -1., 0., -1., -1., -1., -1.,
                   0., -1., -1., 0., 0., 0., 0., -1., -1., -1., 0., 0., 0., 2.]])
    bl = np.array([-inf, -inf, -inf, -inf, -inf, -inf, -inf, -inf, -inf])
    bu = np.array([100., 0., 0., 0., 0., 0., 0., 0., 0.])
    constraints = LinearConstraint(A, bl, bu)
    integrality = 1
    bounds = (0, 1)
    r1 = milp(c=c, constraints=constraints, integrality=integrality, bounds=bounds,
              options={'presolve': True})
    r2 = milp(c=c, constraints=constraints, integrality=integrality, bounds=bounds,
              options={'presolve': False})
    assert r1.status == r2.status
    assert_allclose(r1.fun, r2.fun)

    # another example from the same issue
    bounds = Bounds(lb=0, ub=1)
    integrality = [1, 1, 0, 0]
    c = [10, 9.52380952, -1000, -952.38095238]
    A = [[1, 1, 0, 0], [0, 0, 1, 1], [200, 0, 0, 0], [0, 200, 0, 0],
         [0, 0, 2000, 0], [0, 0, 0, 2000], [-1, 0, 1, 0], [-1, -1, 0, 1]]
    ub = [1, 1, 200, 200, 1000, 1000, 0, 0]
    constraints = LinearConstraint(A, ub=ub)
    r1 = milp(c=c, constraints=constraints,  bounds=bounds,
              integrality=integrality, options={"presolve": False})
    r2 = milp(c=c, constraints=constraints,  bounds=bounds,
              integrality=integrality, options={"presolve": False})
    assert r1.status == r2.status
    assert_allclose(r1.x, r2.x)

