
def test_P32():
    M = Matrix([[1, -2],
                [2, 1]])
    assert exp(M).rewrite(cos).simplify() == Matrix([[E*cos(2), -E*sin(2)],
                                                     [E*sin(2),  E*cos(2)]])

