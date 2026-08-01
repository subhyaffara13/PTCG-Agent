
def test_sample_stochastic_process():
    if not import_module('scipy'):
        skip('SciPy Not installed. Skip sampling tests')
    import random
    random.seed(0)
    numpy = import_module('numpy')
    if numpy:
        numpy.random.seed(0) # scipy uses numpy to sample so to set its seed
    T = Matrix([[0.5, 0.2, 0.3],[0.2, 0.5, 0.3],[0.2, 0.3, 0.5]])
    Y = DiscreteMarkovChain("Y", [0, 1, 2], T)
    for samps in range(10):
        assert next(sample_stochastic_process(Y)) in Y.state_space
    Z = DiscreteMarkovChain("Z", ['1', 1, 0], T)
    for samps in range(10):
        assert next(sample_stochastic_process(Z)) in Z.state_space

    T = Matrix([[S.Half, Rational(1, 4), Rational(1, 4)],
                [Rational(1, 3), 0, Rational(2, 3)],
                [S.Half, S.Half, 0]])
    X = DiscreteMarkovChain('X', [0, 1, 2], T)
    for samps in range(10):
        assert next(sample_stochastic_process(X)) in X.state_space
    W = DiscreteMarkovChain('W', [1, pi, oo], T)
    for samps in range(10):
        assert next(sample_stochastic_process(W)) in W.state_space

