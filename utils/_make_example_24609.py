
def _make_example_24609():
    D, R, H, B_g, V, D_c = symbols("D, R, H, B_g, V, D_c", real=True, positive=True)
    Sigma_f, Sigma_a, nu = symbols("Sigma_f, Sigma_a, nu", real=True, positive=True)
    x = symbols("x", real=True, positive=True)
    eq = (
        2**(S(2)/3)*pi**(S(2)/3)*D_c*(S(231361)/10000 + pi**2/x**2)
        /(6*V**(S(2)/3)*x**(S(1)/3))
      - 2**(S(2)/3)*pi**(S(8)/3)*D_c/(2*V**(S(2)/3)*x**(S(7)/3))
    )
    expected = 100*sqrt(2)*pi/481
    return eq, expected, x

