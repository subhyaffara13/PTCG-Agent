
def test_quaternion_axis_angle():

    test_data = [ # axis, angle, expected_quaternion
        ((1, 0, 0), 0, (1, 0, 0, 0)),
        ((1, 0, 0), pi/2, (sqrt(2)/2, sqrt(2)/2, 0, 0)),
        ((0, 1, 0), pi/2, (sqrt(2)/2, 0, sqrt(2)/2, 0)),
        ((0, 0, 1), pi/2, (sqrt(2)/2, 0, 0, sqrt(2)/2)),
        ((1, 0, 0), pi, (0, 1, 0, 0)),
        ((0, 1, 0), pi, (0, 0, 1, 0)),
        ((0, 0, 1), pi, (0, 0, 0, 1)),
        ((1, 1, 1), pi, (0, 1/sqrt(3),1/sqrt(3),1/sqrt(3))),
        ((sqrt(3)/3, sqrt(3)/3, sqrt(3)/3), pi*2/3, (S.Half, S.Half, S.Half, S.Half))
    ]

    for axis, angle, expected in test_data:
        assert Quaternion.from_axis_angle(axis, angle) == Quaternion(*expected)

