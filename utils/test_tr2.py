
def test_TR2():
    assert TR2(tan(x)) == sin(x)/cos(x)
    assert TR2(cot(x)) == cos(x)/sin(x)
    assert TR2(tan(tan(x) - sin(x)/cos(x))) == 0

