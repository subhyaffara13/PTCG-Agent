from typing import Tuple

def test_dependent_finite():
    X, Y = Die('X'), Die('Y')
    # Dependence testing requires symbolic conditions which currently break
    # finite random variables
    assert dependent(X, Y + X)

    XX, YY = given(Tuple(X, Y), X + Y > 5)  # Create a dependency
    assert dependent(XX, YY)

