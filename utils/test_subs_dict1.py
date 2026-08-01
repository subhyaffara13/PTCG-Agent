
def test_subs_dict1():
    assert (1 + x*y).subs(x, pi) == 1 + pi*y
    assert (1 + x*y).subs({x: pi, y: 2}) == 1 + 2*pi

    c2, c3, q1p, q2p, c1, s1, s2, s3 = symbols('c2 c3 q1p q2p c1 s1 s2 s3')
    test = (c2**2*q2p*c3 + c1**2*s2**2*q2p*c3 + s1**2*s2**2*q2p*c3
            - c1**2*q1p*c2*s3 - s1**2*q1p*c2*s3)
    assert (test.subs({c1**2: 1 - s1**2, c2**2: 1 - s2**2, c3**3: 1 - s3**2})
        == c3*q2p*(1 - s2**2) + c3*q2p*s2**2*(1 - s1**2)
            - c2*q1p*s3*(1 - s1**2) + c3*q2p*s1**2*s2**2 - c2*q1p*s3*s1**2)

