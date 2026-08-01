
def test_basic_plotting_backend():
    x = Symbol('x')
    plot(x, (x, 0, 3), backend='text')
    plot(x**2 + 1, (x, 0, 3), backend='text')

