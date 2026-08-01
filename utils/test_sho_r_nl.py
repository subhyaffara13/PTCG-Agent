
def test_sho_R_nl():
    omega, r = symbols('omega r')
    l = symbols('l', integer=True)
    u = Function('u')

    # check that it obeys the Schrodinger equation
    for n in range(5):
        schreq = ( -diff(u(r), r, 2)/2 + ((l*(l + 1))/(2*r**2)
                    + omega**2*r**2/2 - E_nl(n, l, omega))*u(r) )
        result = schreq.subs(u(r), r*R_nl(n, l, omega/2, r))
        assert simplify(result.doit()) == 0

