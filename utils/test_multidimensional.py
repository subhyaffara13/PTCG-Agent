
def test_multidimensional():
    def f(*x):
        return [3*x[0]**2-2*x[1]**2-1, x[0]**2-2*x[0]+x[1]**2+2*x[1]-8]
    assert mnorm(jacobian(f, (1,-2)) - matrix([[6,8],[0,-2]]),1) < 1.e-7
    for x, error in MDNewton(mp, f, (1,-2), verbose=0,
                             norm=lambda x: norm(x, inf)):
        pass
    assert norm(f(*x), 2) < 1e-14
    # The Chinese mathematician Zhu Shijie was the very first to solve this
    # nonlinear system 700 years ago
    f1 = lambda x, y: -x + 2*y
    f2 = lambda x, y: (x**2 + x*(y**2 - 2) - 4*y)  /  (x + 4)
    f3 = lambda x, y: sqrt(x**2 + y**2)
    def f(x, y):
        f1x = f1(x, y)
        return (f2(x, y) - f1x, f3(x, y) - f1x)
    x = findroot(f, (10, 10))
    assert [int(round(i)) for i in x] == [3, 4]

