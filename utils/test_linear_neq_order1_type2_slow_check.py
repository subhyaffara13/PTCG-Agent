
def test_linear_neq_order1_type2_slow_check():
    RC, t, C, Vs, L, R1, V0, I0 = symbols("RC t C Vs L R1 V0 I0")
    V = Function("V")
    I = Function("I")
    system = [Eq(V(t).diff(t), -1/RC*V(t) + I(t)/C), Eq(I(t).diff(t), -R1/L*I(t) - 1/L*V(t) + Vs/L)]
    [sol] = dsolve_system(system, simplify=False, doit=False)

    assert checksysodesol(system, sol) == (True, [0, 0])

