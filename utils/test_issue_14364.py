
def test_issue_14364():
    assert gcd(S(6)*(1 + sqrt(3))/5, S(3)*(1 + sqrt(3))/10) == Rational(3, 10) * (1 + sqrt(3))
    assert gcd(sqrt(5)*Rational(4, 7), sqrt(5)*Rational(2, 3)) == sqrt(5)*Rational(2, 21)

    assert lcm(Rational(2, 3)*sqrt(3), Rational(5, 6)*sqrt(3)) == S(10)*sqrt(3)/3
    assert lcm(3*sqrt(3), 4/sqrt(3)) == 12*sqrt(3)
    assert lcm(S(5)*(1 + 2**Rational(1, 3))/6, S(3)*(1 + 2**Rational(1, 3))/8) == Rational(15, 2) * (1 + 2**Rational(1, 3))

    assert gcd(Rational(2, 3)*sqrt(3), Rational(5, 6)/sqrt(3)) == sqrt(3)/18
    assert gcd(S(4)*sqrt(13)/7, S(3)*sqrt(13)/14) == sqrt(13)/14

    # gcd_list and lcm_list
    assert gcd([S(2)*sqrt(47)/7, S(6)*sqrt(47)/5, S(8)*sqrt(47)/5]) == sqrt(47)*Rational(2, 35)
    assert gcd([S(6)*(1 + sqrt(7))/5, S(2)*(1 + sqrt(7))/7, S(4)*(1 + sqrt(7))/13]) ==  (1 + sqrt(7))*Rational(2, 455)
    assert lcm((Rational(7, 2)/sqrt(15), Rational(5, 6)/sqrt(15), Rational(5, 8)/sqrt(15))) == Rational(35, 2)/sqrt(15)
    assert lcm([S(5)*(2 + 2**Rational(5, 7))/6, S(7)*(2 + 2**Rational(5, 7))/2, S(13)*(2 + 2**Rational(5, 7))/4]) == Rational(455, 2) * (2 + 2**Rational(5, 7))

