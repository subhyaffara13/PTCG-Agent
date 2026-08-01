
def test_imag():
    I = S('I')
    assert julia_code(I) == "im"
    assert julia_code(5*I) == "5im"
    assert julia_code((S(3)/2)*I) == "(3 // 2) * im"
    assert julia_code(3+4*I) == "3 + 4im"


def test_imag():
    I = S('I')
    assert maple_code(I) == "I"
    assert maple_code(5 * I) == "5*I"

    assert maple_code((S(3) / 2) * I) == "(3/2)*I"
    assert maple_code(3 + 4 * I) == "3 + 4*I"


def test_imag():
    I = S('I')
    assert mcode(I) == "1i"
    assert mcode(5*I) == "5i"
    assert mcode((S(3)/2)*I) == "3*1i/2"
    assert mcode(3+4*I) == "3 + 4i"
    assert mcode(sqrt(3)*I) == "sqrt(3)*1i"

