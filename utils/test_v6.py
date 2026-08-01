
def test_V6():
    # returns RootSum(40*_z**2 - 1, Lambda(_i, _i*log(-4*_i + exp(-m*x))))/m
    assert (integrate(1/(2*exp(m*x) - 5*exp(-m*x)), x) == sqrt(10)*(
            log(2*exp(m*x) - sqrt(10)) - log(2*exp(m*x) + sqrt(10)))/(20*m))

