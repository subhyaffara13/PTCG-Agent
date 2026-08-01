
def test_issue_8247_8354():
    from sympy.functions.elementary.trigonometric import tan
    z = sqrt(1 + sqrt(3)) + sqrt(3 + 3*sqrt(3)) - sqrt(10 + 6*sqrt(3))
    assert z.is_positive is False  # it's 0
    z = S('''-2**(1/3)*(3*sqrt(93) + 29)**2 - 4*(3*sqrt(93) + 29)**(4/3) +
        12*sqrt(93)*(3*sqrt(93) + 29)**(1/3) + 116*(3*sqrt(93) + 29)**(1/3) +
        174*2**(1/3)*sqrt(93) + 1678*2**(1/3)''')
    assert z.is_positive is False  # it's 0
    z = 2*(-3*tan(19*pi/90) + sqrt(3))*cos(11*pi/90)*cos(19*pi/90) - \
        sqrt(3)*(-3 + 4*cos(19*pi/90)**2)
    assert z.is_positive is not True  # it's zero and it shouldn't hang
    z = S('''9*(3*sqrt(93) + 29)**(2/3)*((3*sqrt(93) +
        29)**(1/3)*(-2**(2/3)*(3*sqrt(93) + 29)**(1/3) - 2) - 2*2**(1/3))**3 +
        72*(3*sqrt(93) + 29)**(2/3)*(81*sqrt(93) + 783) + (162*sqrt(93) +
        1566)*((3*sqrt(93) + 29)**(1/3)*(-2**(2/3)*(3*sqrt(93) + 29)**(1/3) -
        2) - 2*2**(1/3))**2''')
    assert z.is_positive is False  # it's 0 (and a single _mexpand isn't enough)

