
def test_quaternion_axis_angle_simplification():
    result = Quaternion.from_axis_angle((1, 2, 3), asin(4))
    assert result.a == cos(asin(4)/2)
    assert result.b == sqrt(14)*sin(asin(4)/2)/14
    assert result.c == sqrt(14)*sin(asin(4)/2)/7
    assert result.d == 3*sqrt(14)*sin(asin(4)/2)/14

