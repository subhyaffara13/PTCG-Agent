
def test_to_euler_numerical_singilarities():

    def test_one_case(angles, seq):
        q = Quaternion.from_euler(angles, seq)
        assert q.to_euler(seq) == angles

    # symmetric
    test_one_case((pi/2,  0, 0), 'zyz')
    test_one_case((pi/2,  0, 0), 'ZYZ')
    test_one_case((pi/2,  pi, 0), 'zyz')
    test_one_case((pi/2,  pi, 0), 'ZYZ')

    # asymmetric
    test_one_case((pi/2,  pi/2, 0), 'zyx')
    test_one_case((pi/2,  -pi/2, 0), 'zyx')
    test_one_case((pi/2,  pi/2, 0), 'ZYX')
    test_one_case((pi/2,  -pi/2, 0), 'ZYX')

