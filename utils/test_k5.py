
def test_K5():
    x, y = symbols('x, y', real=True)
    assert tan(x + I*y).expand(complex=True) == (sin(2*x)/(cos(2*x) +
        cosh(2*y)) + I*sinh(2*y)/(cos(2*x) + cosh(2*y)))


def test_K5(graph):
    """Maximal independent set for complete graphs"""
    assert all(nx.maximal_independent_set(graph, [n]) == [n] for n in graph)

