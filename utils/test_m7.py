
def test_M7():
    # TODO: Replace solve with solveset, as of now test fails for solveset
    assert set(solve(x**8 - 8*x**7 + 34*x**6 - 92*x**5 + 175*x**4 - 236*x**3 +
        226*x**2 - 140*x + 46, x)) == {
        1 - sqrt(2)*I*sqrt(-sqrt(-3 + 4*sqrt(3)) + 3)/2,
        1 - sqrt(2)*sqrt(-3 + I*sqrt(3 + 4*sqrt(3)))/2,
        1 - sqrt(2)*I*sqrt(sqrt(-3 + 4*sqrt(3)) + 3)/2,
        1 - sqrt(2)*sqrt(-3 - I*sqrt(3 + 4*sqrt(3)))/2,
        1 + sqrt(2)*I*sqrt(sqrt(-3 + 4*sqrt(3)) + 3)/2,
        1 + sqrt(2)*sqrt(-3 - I*sqrt(3 + 4*sqrt(3)))/2,
        1 + sqrt(2)*sqrt(-3 + I*sqrt(3 + 4*sqrt(3)))/2,
        1 + sqrt(2)*I*sqrt(-sqrt(-3 + 4*sqrt(3)) + 3)/2,
        }

