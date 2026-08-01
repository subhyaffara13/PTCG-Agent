
def test_uselogcombine_2():
    eq = log(exp(2*x) + 1) + log(-tanh(x) + 1) - log(2)
    assert solveset_real(eq, x) is S.EmptySet
    eq = log(8*x) - log(sqrt(x) + 1) - 2
    assert solveset_real(eq, x) is S.EmptySet

