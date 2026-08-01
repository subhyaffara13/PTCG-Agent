
def test_issue_26161():
    # Issue https://github.com/sympy/sympy/issues/26161
    Ib, Is, m, h, l2, l1 = symbols('I_b, I_s, m, h, l2, l1',
                                            real=True, nonnegative=True)
    KD, KP, v = symbols('K_D, K_P, v', real=True)

    tau1_sq = (Ib + m * h ** 2) / m / g / h
    tau2 = l2 / v
    tau3 = v / (l1 + l2)
    K = v ** 2 / g / (l1 + l2)

    Gtheta = TransferFunction(-K * (tau2 * s + 1), tau1_sq * s ** 2 - 1, s)
    Gdelta = TransferFunction(1, Is * s ** 2 + c * s, s)
    Gpsi = TransferFunction(1, tau3 * s, s)
    Dcont = TransferFunction(KD * s, 1, s)
    PIcont = TransferFunction(KP, s, s)
    Gunity = TransferFunction(1, 1, s)

    Ginner = Feedback(Dcont * Gdelta, Gtheta)
    Gouter = Feedback(PIcont * Ginner * Gpsi, Gunity)
    assert Gouter == Feedback(Series(PIcont, Series(Ginner, Gpsi)), Gunity)
    assert Gouter.num == Series(PIcont, Series(Ginner, Gpsi))
    assert Gouter.den == Parallel(Gunity, Series(Gunity, Series(PIcont, Series(Ginner, Gpsi))))
    expr = (KD*KP*g*s**3*v**2*(l1 + l2)*(Is*s**2 + c*s)**2*(-g*h*m + s**2*(Ib + h**2*m))*(-KD*g*h*m*s*v**2*(l2*s + v) + \
            g*v*(l1 + l2)*(Is*s**2 + c*s)*(-g*h*m + s**2*(Ib + h**2*m))))/((s**2*v*(Is*s**2 + c*s)*(-KD*g*h*m*s*v**2* \
            (l2*s + v) + g*v*(l1 + l2)*(Is*s**2 + c*s)*(-g*h*m + s**2*(Ib + h**2*m)))*(KD*KP*g*s*v*(l1 + l2)**2* \
            (Is*s**2 + c*s)*(-g*h*m + s**2*(Ib + h**2*m)) + s**2*v*(Is*s**2 + c*s)*(-KD*g*h*m*s*v**2*(l2*s + v) + \
            g*v*(l1 + l2)*(Is*s**2 + c*s)*(-g*h*m + s**2*(Ib + h**2*m))))/(l1 + l2)))

    assert (Gouter.to_expr() - expr).simplify() == 0

