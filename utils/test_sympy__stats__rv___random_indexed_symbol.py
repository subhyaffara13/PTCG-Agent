
def test_sympy__stats__rv__RandomIndexedSymbol():
    from sympy.stats.rv import RandomIndexedSymbol, pspace
    from sympy.stats.stochastic_process_types import DiscreteMarkovChain
    X = DiscreteMarkovChain("X")
    assert _test_args(RandomIndexedSymbol(X[0].symbol, pspace(X[0])))

