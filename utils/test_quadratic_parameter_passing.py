
def test_quadratic_parameter_passing():
    eq = -33*x*y + 3*y**2
    solution = BinaryQuadratic(eq).solve(parameters=[t, u])
    # test that parameters are passed all the way to the final solution
    assert solution == {(t, 11*t), (t, -22*t)}
    assert solution(0, 0) == {(0, 0)}

