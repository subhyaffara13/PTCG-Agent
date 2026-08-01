
def test_T9():
    z, k = symbols('z k', positive=True)
    # raises NotImplementedError:
    #           Don't know how to calculate the mrv of '(1, k)'
    assert limit(hyper((1, k), (1,), z/k), k, oo) == exp(z)

