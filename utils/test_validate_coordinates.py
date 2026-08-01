
def test_validate_coordinates():
    q1, q2, q3, u1, u2, u3, ua1, ua2, ua3 = dynamicsymbols('q1:4 u1:4 ua1:4')
    s1, s2, s3 = symbols('s1:4')
    # Test normal
    _validate_coordinates([q1, q2, q3], [u1, u2, u3],
                          u_auxiliary=[ua1, ua2, ua3])
    # Test not equal number of coordinates and speeds
    _validate_coordinates([q1, q2])
    _validate_coordinates([q1, q2], [u1])
    _validate_coordinates(speeds=[u1, u2])
    # Test duplicate
    _validate_coordinates([q1, q2, q2], [u1, u2, u3], check_duplicates=False)
    raises(ValueError, lambda: _validate_coordinates(
        [q1, q2, q2], [u1, u2, u3]))
    _validate_coordinates([q1, q2, q3], [u1, u2, u2], check_duplicates=False)
    raises(ValueError, lambda: _validate_coordinates(
        [q1, q2, q3], [u1, u2, u2], check_duplicates=True))
    raises(ValueError, lambda: _validate_coordinates(
        [q1, q2, q3], [q1, u2, u3], check_duplicates=True))
    _validate_coordinates([q1, q2, q3], [u1, u2, u3], check_duplicates=False,
                          u_auxiliary=[u1, ua2, ua2])
    raises(ValueError, lambda: _validate_coordinates(
        [q1, q2, q3], [u1, u2, u3], u_auxiliary=[u1, ua2, ua3]))
    raises(ValueError, lambda: _validate_coordinates(
        [q1, q2, q3], [u1, u2, u3], u_auxiliary=[q1, ua2, ua3]))
    raises(ValueError, lambda: _validate_coordinates(
        [q1, q2, q3], [u1, u2, u3], u_auxiliary=[ua1, ua2, ua2]))
    # Test is_dynamicsymbols
    _validate_coordinates([q1 + q2, q3], is_dynamicsymbols=False)
    raises(ValueError, lambda: _validate_coordinates([q1 + q2, q3]))
    _validate_coordinates([s1, q1, q2], [0, u1, u2], is_dynamicsymbols=False)
    raises(ValueError, lambda: _validate_coordinates(
        [s1, q1, q2], [0, u1, u2], is_dynamicsymbols=True))
    _validate_coordinates([s1 + s2 + s3, q1], [0, u1], is_dynamicsymbols=False)
    raises(ValueError, lambda: _validate_coordinates(
        [s1 + s2 + s3, q1], [0, u1], is_dynamicsymbols=True))
    _validate_coordinates(u_auxiliary=[s1, ua1], is_dynamicsymbols=False)
    raises(ValueError, lambda: _validate_coordinates(u_auxiliary=[s1, ua1]))
    # Test normal function
    t = dynamicsymbols._t
    a = symbols('a')
    f1, f2 = symbols('f1:3', cls=Function)
    _validate_coordinates([f1(a), f2(a)], is_dynamicsymbols=False)
    raises(ValueError, lambda: _validate_coordinates([f1(a), f2(a)]))
    raises(ValueError, lambda: _validate_coordinates(speeds=[f1(a), f2(a)]))
    dynamicsymbols._t = a
    _validate_coordinates([f1(a), f2(a)])
    raises(ValueError, lambda: _validate_coordinates([f1(t), f2(t)]))
    dynamicsymbols._t = t

