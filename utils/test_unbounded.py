
def test_unbounded():
    assert ask(Q.infinite(I * oo)) is True
    assert ask(Q.infinite(1 + I*oo)) is True
    assert ask(Q.infinite(3 * (I * oo))) is True
    assert ask(Q.infinite(-I * oo)) is True
    assert ask(Q.infinite(1 + zoo)) is True
    assert ask(Q.infinite(I * zoo)) is True
    assert ask(Q.infinite(x / y), Q.infinite(x) & Q.finite(y) & ~Q.zero(y)) is True
    assert ask(Q.infinite(I * oo - I * oo)) is None
    assert ask(Q.infinite(x * I * oo)) is None
    assert ask(Q.infinite(1 / x), Q.finite(x) & ~Q.zero(x)) is False
    assert ask(Q.infinite(1 / (I * oo))) is False


def test_unbounded():
    G = nx.complete_graph(5)
    for flow_func in flow_funcs:
        assert 4 == len(minimum_st_edge_cut(G, 1, 4, flow_func=flow_func))

