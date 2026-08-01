
def test_issue_3210():
    eqs = (sin(2)*cos(3) + sin(3)*cos(2),
        -sin(2)*sin(3) + cos(2)*cos(3),
        sin(2)*cos(3) - sin(3)*cos(2),
        sin(2)*sin(3) + cos(2)*cos(3),
        sin(2)*sin(3) + cos(2)*cos(3) + cos(2),
        sinh(2)*cosh(3) + sinh(3)*cosh(2),
        sinh(2)*sinh(3) + cosh(2)*cosh(3),
        )
    assert [trigsimp(e) for e in eqs] == [
        sin(5),
        cos(5),
        -sin(1),
        cos(1),
        cos(1) + cos(2),
        sinh(5),
        cosh(5),
        ]

