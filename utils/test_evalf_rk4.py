
def test_evalf_rk4():
    x = symbols('x')
    R, Dx = DifferentialOperators(QQ.old_poly_ring(x), 'Dx')

    # log(1+x)
    p = HolonomicFunction((1 + x)*Dx**2 + Dx, x, 0, [0, 1])

    # path taken is a straight line from 0 to 1, on the real axis
    r = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    s = '0.693146363174626'  # approx. equal to log(2) i.e. 0.693147180559945
    assert sstr(p.evalf(r)[-1]) == s

    # path taken is a triangle 0-->1+i-->2
    r = [0.1 + 0.1*I]
    for i in range(9):
        r.append(r[-1]+0.1+0.1*I)
    for i in range(10):
        r.append(r[-1]+0.1-0.1*I)

    # close to the exact solution 1.09861228866811
    # imaginary part also close to zero
    s = '1.098616 + 1.36083e-7*I'
    assert sstr(p.evalf(r)[-1].n(7)) == s

    # sin(x)
    p = HolonomicFunction(Dx**2 + 1, x, 0, [0, 1])
    s = '0.90929463522785 + 1.52655665885959e-16*I'
    assert sstr(p.evalf(r)[-1]) == s

    # computing sin(pi/2) using this method
    # using a linear path from 0 to pi/2
    r = [0.1]
    for i in range(14):
        r.append(r[-1] + 0.1)
    r.append(pi/2)
    s = '0.999999895088917' # close to 1.0 (exact solution)
    assert sstr(p.evalf(r)[-1]) == s

    # trying different path, a rectangle (0-->i-->pi/2 + i-->pi/2)
    # computing the same value sin(pi/2) using different path
    r = [0.1*I]
    for i in range(9):
        r.append(r[-1]+0.1*I)
    for i in range(15):
        r.append(r[-1]+0.1)
    r.append(pi/2+I)
    for i in range(10):
        r.append(r[-1]-0.1*I)

    # close to 1.0
    s = '1.00000003415141 + 6.11940487991086e-16*I'
    assert sstr(p.evalf(r)[-1]) == s

    # cos(x)
    p = HolonomicFunction(Dx**2 + 1, x, 0, [1, 0])
    # compute cos(pi) along 0-->pi
    r = [0.05]
    for i in range(61):
        r.append(r[-1]+0.05)
    r.append(pi)
    # close to -1 (exact answer)
    s = '-0.999999993238714'
    assert sstr(p.evalf(r)[-1]) == s

    # a rectangular path (0 -> i -> 2+i -> 2)
    r = [0.1*I]
    for i in range(9):
        r.append(r[-1]+0.1*I)
    for i in range(20):
        r.append(r[-1]+0.1)
    for i in range(10):
        r.append(r[-1]-0.1*I)

    p = HolonomicFunction(Dx**2 + 1, x, 0, [1,1]).evalf(r)
    s = '0.493152791638442 - 1.41553435639707e-15*I'
    assert sstr(p[-1]) == s

