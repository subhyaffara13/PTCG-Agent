
def test_factor_system():

    assert factor_system([x**2 + 2*x + 1]) ==  [[x + 1]]
    assert factor_system([x**2 + 2*x + 1, y**2 + 2*y + 1]) ==  [[x + 1, y + 1]]
    assert factor_system([x**2 + 1]) ==  [[x**2 + 1]]
    assert factor_system([]) == [[]]

    assert factor_system([x**2 + y**2 + 2*x*y, x**2 - 2], extension=sqrt(2)) == [
        [x + y, x + sqrt(2)],
        [x + y, x - sqrt(2)],
    ]

    assert factor_system([x**2 + 1, y**2 + 1], gaussian=True) == [
        [x + I, y + I],
        [x + I, y - I],
        [x - I, y + I],
        [x - I, y - I],
    ]

    assert factor_system([x**2 + 1, y**2 + 1], domain=QQ_I) == [
        [x + I, y + I],
        [x + I, y - I],
        [x - I, y + I],
        [x - I, y - I],
    ]

    assert factor_system([0]) == [[]]
    assert factor_system([1]) == []
    assert factor_system([0 , x]) == [[x]]
    assert factor_system([1, 0, x]) == []

    assert factor_system([x**4 - 1, y**6 - 1]) == [
        [x**2 + 1, y**2 + y + 1],
        [x**2 + 1, y**2 - y + 1],
        [x**2 + 1, y + 1],
        [x**2 + 1, y - 1],
        [x + 1, y**2 + y + 1],
        [x + 1, y**2 - y + 1],
        [x - 1, y**2 + y + 1],
        [x - 1, y**2 - y + 1],
        [x + 1, y + 1],
        [x + 1, y - 1],
        [x - 1, y + 1],
        [x - 1, y - 1],
    ]

    assert factor_system([(x - 1)*(y - 2), (y - 2)*(z - 3)]) == [
        [x - 1, z - 3],
        [y - 2]
    ]

    assert factor_system([sin(x)**2 + cos(x)**2 - 1, x]) == [
        [x, sin(x)**2 + cos(x)**2 - 1],
    ]

    assert factor_system([sin(x)**2 + cos(x)**2 - 1]) == [
        [sin(x)**2 + cos(x)**2 - 1]
    ]

    assert factor_system([sin(x)**2 + cos(x)**2]) == [
        [sin(x)**2 + cos(x)**2]
    ]

    assert factor_system([a*x, y, a]) == [[y, a]]

    assert factor_system([a*x, y, a], [x, y]) == []

    assert factor_system([a ** 2 * x, y], [x, y]) == [[x, y]]

    assert factor_system([a*x*(x - 1), b*y, c], [x, y]) == []

    assert factor_system([a*x*(x - 1), b*y, c], [x, y, c]) == [
        [x - 1, y, c],
        [x, y, c],
    ]

    assert factor_system([a*x*(x - 1), b*y, c]) == [
        [x - 1, y, c],
        [x, y, c],
        [x - 1, b, c],
        [x, b, c],
        [y, a, c],
        [a, b, c],
    ]

    assert factor_system([x**2 - 2], [y]) == []

    assert factor_system([x**2 - 2], [x]) == [[x**2 - 2]]

    assert factor_system([cos(x)**2 - sin(x)**2, cos(x)**2 + sin(x)**2 - 1]) == [
        [sin(x)**2 + cos(x)**2 - 1, sin(x) + cos(x)],
        [sin(x)**2 + cos(x)**2 - 1, -sin(x) + cos(x)],
    ]

    assert factor_system([(cos(x) + sin(x))**2 - 1, cos(x)**2 - sin(x)**2 - cos(2*x)]) == [
        [sin(x)**2 - cos(x)**2 + cos(2*x), sin(x) + cos(x) + 1],
        [sin(x)**2 - cos(x)**2 + cos(2*x), sin(x) + cos(x) - 1],
    ]

    assert factor_system([(cos(x) + sin(x))*exp(y) - 1, (cos(x) - sin(x))*exp(y) - 1]) == [
        [exp(y)*sin(x) + exp(y)*cos(x) - 1, -exp(y)*sin(x) + exp(y)*cos(x) - 1]
    ]

