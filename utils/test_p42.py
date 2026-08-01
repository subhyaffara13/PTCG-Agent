
def test_P42():
    assert wronskian([cos(x), sin(x)], x).simplify() == 1

