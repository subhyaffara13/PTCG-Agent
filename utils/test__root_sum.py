
def test_RootSum():
    f = x**5 + 2*x - 1

    assert str(
        RootSum(f, Lambda(z, z), auto=False)) == "RootSum(x**5 + 2*x - 1)"
    assert str(RootSum(f, Lambda(
        z, z**2), auto=False)) == "RootSum(x**5 + 2*x - 1, Lambda(z, z**2))"

