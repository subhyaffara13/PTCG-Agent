
def test_issue_5547():
    L = Symbol('L')
    z = Symbol('z')
    r0 = Symbol('r0')
    R0 = Symbol('R0')

    assert integrate(r0**2*cos(z)**2, (z, -L/2, L/2)) == -r0**2*(-L/4 -
                    sin(L/2)*cos(L/2)/2) + r0**2*(L/4 + sin(L/2)*cos(L/2)/2)

    assert integrate(r0**2*cos(R0*z)**2, (z, -L/2, L/2)) == Piecewise(
        (-r0**2*(-L*R0/4 - sin(L*R0/2)*cos(L*R0/2)/2)/R0 +
         r0**2*(L*R0/4 + sin(L*R0/2)*cos(L*R0/2)/2)/R0, (R0 > -oo) & (R0 < oo) & Ne(R0, 0)),
        (L*r0**2, True))

    w = 2*pi*z/L

    sol = sqrt(2)*sqrt(L)*r0**2*fresnelc(sqrt(2)*sqrt(L))*gamma(S.One/4)/(16*gamma(S(5)/4)) + L*r0**2/2

    assert integrate(r0**2*cos(w*z)**2, (z, -L/2, L/2)) == sol

