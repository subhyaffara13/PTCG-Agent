
def test_issue_2708():
    # This test needs to use an integration function that can
    # not be evaluated in closed form.  Update as needed.
    f = 1/(a + z + log(z))
    integral_f = NonElementaryIntegral(f, (z, 2, 3))
    assert Integral(f, (z, 2, 3)).doit() == integral_f
    assert integrate(f + exp(z), (z, 2, 3)) == integral_f - exp(2) + exp(3)
    assert integrate(2*f + exp(z), (z, 2, 3)) == \
        2*integral_f - exp(2) + exp(3)
    assert integrate(exp(1.2*n*s*z*(-t + z)/t), (z, 0, x)) == \
        NonElementaryIntegral(exp(-1.2*n*s*z)*exp(1.2*n*s*z**2/t),
                                  (z, 0, x))

