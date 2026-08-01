
def test_1():
    from sympy.abc import x
    print_gtk(x**2, start_viewer=False)
    print_gtk(x**2 + sin(x)/4, start_viewer=False)


def test_1():
    def f(x):
        return x**4, 4*x**3

    for gtol in [1e-8, 1e-12, 1e-20]:
        for maxcor in range(20, 35):
            result = minimize(fun=f, jac=True, method='L-BFGS-B', x0=20,
                options={'gtol': gtol, 'maxcor': maxcor})

            H1 = result.hess_inv(np.array([1])).reshape(1,1)
            H2 = result.hess_inv.todense()

            assert_allclose(H1, H2)

