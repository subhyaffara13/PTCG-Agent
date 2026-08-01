
def test_aug_assign():
    x = symbols('x')
    assert fcode(aug_assign(x, '+', 1), source_format='free') == 'x = x + 1'

