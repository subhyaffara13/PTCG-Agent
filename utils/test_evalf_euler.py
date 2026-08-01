
def test_evalf_euler():
    x = symbols('x')
    R, Dx = DifferentialOperators(QQ.old_poly_ring(x), 'Dx')

    # log(1+x)
    p = HolonomicFunction((1 + x)*Dx**2 + Dx, x, 0, [0, 1])

    # path taken is a straight line from 0 to 1, on the real axis
    r = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    s = '0.699525841805253'  # approx. equal to log(2) i.e. 0.693147180559945
    assert sstr(p.evalf(r, method='Euler')[-1]) == s

    # path taken is a triangle 0-->1+i-->2
    r = [0.1 + 0.1*I]
    for i in range(9):
        r.append(r[-1]+0.1+0.1*I)
    for i in range(10):
        r.append(r[-1]+0.1-0.1*I)

    # close to the exact solution 1.09861228866811
    # imaginary part also close to zero
    s = '1.07530466271334 - 0.0251200594793912*I'
    assert sstr(p.evalf(r, method='Euler')[-1]) == s

    # sin(x)
    p = HolonomicFunction(Dx**2 + 1, x, 0, [0, 1])
    s = '0.905546532085401 - 6.93889390390723e-18*I'
    assert sstr(p.evalf(r, method='Euler')[-1]) == s

    # computing sin(pi/2) using this method
    # using a linear path from 0 to pi/2
    r = [0.1]
    for i in range(14):
        r.append(r[-1] + 0.1)
    r.append(pi/2)
    s = '1.08016557252834' # close to 1.0 (exact solution)
    assert sstr(p.evalf(r, method='Euler')[-1]) == s

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
    s = '0.976882381836257 - 1.65557671738537e-16*I'
    assert sstr(p.evalf(r, method='Euler')[-1]) == s

    # cos(x)
    p = HolonomicFunction(Dx**2 + 1, x, 0, [1, 0])
    # compute cos(pi) along 0-->pi
    r = [0.05]
    for i in range(61):
        r.append(r[-1]+0.05)
    r.append(pi)
    # close to -1 (exact answer)
    s = '-1.08140824719196'
    assert sstr(p.evalf(r, method='Euler')[-1]) == s

    # a rectangular path (0 -> i -> 2+i -> 2)
    r = [0.1*I]
    for i in range(9):
        r.append(r[-1]+0.1*I)
    for i in range(20):
        r.append(r[-1]+0.1)
    for i in range(10):
        r.append(r[-1]-0.1*I)

    p = HolonomicFunction(Dx**2 + 1, x, 0, [1,1]).evalf(r, method='Euler')
    s = '0.501421652861245 - 3.88578058618805e-16*I'
    assert sstr(p[-1]) == s

