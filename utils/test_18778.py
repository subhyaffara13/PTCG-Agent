
def test_18778():
    raises(TypeError, lambda: is_le(Basic(), Basic()))
    raises(TypeError, lambda: is_gt(Basic(), Basic()))
    raises(TypeError, lambda: is_ge(Basic(), Basic()))
    raises(TypeError, lambda: is_lt(Basic(), Basic()))

