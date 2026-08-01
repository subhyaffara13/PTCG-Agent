
def test_square_factor():
    assert square_factor(1) == square_factor(-1) == 1
    assert square_factor(0) == 1
    assert square_factor(5) == square_factor(-5) == 1
    assert square_factor(4) == square_factor(-4) == 2
    assert square_factor(12) == square_factor(-12) == 2
    assert square_factor(6) == 1
    assert square_factor(18) == 3
    assert square_factor(52) == 2
    assert square_factor(49) == 7
    assert square_factor(392) == 14
    assert square_factor(factorint(-12)) == 2

