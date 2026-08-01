
def test_nonlinsolve_inexact():
    sol = [(-1.625, -1.375), (1.625, 1.375)]
    res = nonlinsolve([(x + y)**2 - 9, x**2 - y**2 - 0.75], [x, y])
    assert all(abs(res.args[i][j]-sol[i][j]) < 1e-9
               for i in range(2) for j in range(2))

    assert nonlinsolve([(x + y)**2 - 9, (x + y)**2 - 0.75], [x, y]) == S.EmptySet

    assert nonlinsolve([y**2 + (x - 0.5)**2 - 0.0625, 2*x - 1.0, 2*y], [x, y]) == \
           S.EmptySet

    res = nonlinsolve([x**2 + y - 0.5, (x + y)**2, log(z)], [x, y, z])
    sol = [(-0.366025403784439, 0.366025403784439, 1),
           (-0.366025403784439, 0.366025403784439, 1),
           (1.36602540378444, -1.36602540378444, 1)]
    assert all(abs(res.args[i][j]-sol[i][j]) < 1e-9
               for i in range(3) for j in range(3))

    res = nonlinsolve([y - x**2, x**5 - x + 1.0], [x, y])
    sol = [(-1.16730397826142, 1.36259857766493),
           (-0.181232444469876 - 1.08395410131771*I,
            -1.14211129483496 + 0.392895302949911*I),
           (-0.181232444469876 + 1.08395410131771*I,
            -1.14211129483496 - 0.392895302949911*I),
           (0.764884433600585 - 0.352471546031726*I,
            0.460812006002492 - 0.539199997693599*I),
           (0.764884433600585 + 0.352471546031726*I,
            0.460812006002492 + 0.539199997693599*I)]
    assert all(abs(res.args[i][j] - sol[i][j]) < 1e-9
               for i in range(5) for j in range(2))

