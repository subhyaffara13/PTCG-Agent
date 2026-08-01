
def test_Limit_dir():
    raises(TypeError, lambda: Limit(x, x, 0, dir=0))
    raises(ValueError, lambda: Limit(x, x, 0, dir='0'))

