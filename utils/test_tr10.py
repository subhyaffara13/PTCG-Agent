
def test_TR10():
    assert TR10(cos(a + b)) == -sin(a)*sin(b) + cos(a)*cos(b)
    assert TR10(sin(a + b)) == sin(a)*cos(b) + sin(b)*cos(a)
    assert TR10(sin(a + b + c)) == \
        (-sin(a)*sin(b) + cos(a)*cos(b))*sin(c) + \
        (sin(a)*cos(b) + sin(b)*cos(a))*cos(c)
    assert TR10(cos(a + b + c)) == \
        (-sin(a)*sin(b) + cos(a)*cos(b))*cos(c) - \
        (sin(a)*cos(b) + sin(b)*cos(a))*sin(c)

