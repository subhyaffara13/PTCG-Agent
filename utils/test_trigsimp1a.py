
def test_trigsimp1a():
    assert trigsimp(sin(2)**2*cos(3)*exp(2)/cos(2)**2) == tan(2)**2*cos(3)*exp(2)
    assert trigsimp(tan(2)**2*cos(3)*exp(2)*cos(2)**2) == sin(2)**2*cos(3)*exp(2)
    assert trigsimp(cot(2)*cos(3)*exp(2)*sin(2)) == cos(3)*exp(2)*cos(2)
    assert trigsimp(tan(2)*cos(3)*exp(2)/sin(2)) == cos(3)*exp(2)/cos(2)
    assert trigsimp(cot(2)*cos(3)*exp(2)/cos(2)) == cos(3)*exp(2)/sin(2)
    assert trigsimp(cot(2)*cos(3)*exp(2)*tan(2)) == cos(3)*exp(2)
    assert trigsimp(sinh(2)*cos(3)*exp(2)/cosh(2)) == tanh(2)*cos(3)*exp(2)
    assert trigsimp(tanh(2)*cos(3)*exp(2)*cosh(2)) == sinh(2)*cos(3)*exp(2)
    assert trigsimp(coth(2)*cos(3)*exp(2)*sinh(2)) == cosh(2)*cos(3)*exp(2)
    assert trigsimp(tanh(2)*cos(3)*exp(2)/sinh(2)) == cos(3)*exp(2)/cosh(2)
    assert trigsimp(coth(2)*cos(3)*exp(2)/cosh(2)) == cos(3)*exp(2)/sinh(2)
    assert trigsimp(coth(2)*cos(3)*exp(2)*tanh(2)) == cos(3)*exp(2)

