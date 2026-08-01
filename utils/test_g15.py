
def test_G15():
    assert Rational(sqrt(3).evalf()).limit_denominator(15) == R(26, 15)
    assert list(takewhile(lambda x: x.q <= 15, cf_c(cf_i(sqrt(3)))))[-1] == \
        R(26, 15)

