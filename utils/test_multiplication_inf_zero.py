
def test_multiplication_inf_zero():

    M = Matrix([[oo, 0], [0, oo]])
    assert M ** 2 == M

    M = Matrix([[oo, oo], [0, 0]])
    assert M ** 2 == Matrix([[nan, nan], [nan, nan]])

    A = Matrix([
        [0, 0, 0, -S(1)/2],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [-S(1)/2, 0, 0, 0]])

    B = Matrix([
        [pi*x**2, 0, pi*b*x**4/8 + pi*a*x**4/8 + O(x**5), pi*x**4/2 + pi*b**2*x**6/32 + pi*a*b*x**6/48 + pi*a**2*x**6/32 + O(x**7)],
        [0, pi*x**4/4, O(x**6), O(x**8)],
        [pi*b*x**4/8 + pi*a*x**4/8 + O(x**5), O(x**6), pi*b**2*x**6/32 + pi*a*b*x**6/48 + pi*a**2*x**6/32 + O(x**7), pi*b*x**6/12 + pi*a*x**6/12 + O(x**7)],
        [pi*x**4/2 + pi*b**2*x**6/32 + pi*a*b*x**6/48 + pi*a**2*x**6/32 + O(x**7), O(x**8), pi*b*x**6/12 + pi*a*x**6/12 + O(x**7), pi*x**6/3 + 3*pi*b**2*x**8/64 + pi*a*b*x**8/32 + 3*pi*a**2*x**8/64 + O(x**9)]])

    C = Matrix([
    [-pi*x**4/4 - pi*b**2*x**6/64 - pi*a*b*x**6/96 - pi*a**2*x**6/64 + O(x**7),   O(x**8),                       -pi*b*x**6/24 - pi*a*x**6/24 + O(x**7), -pi*x**6/6 - 3*pi*b**2*x**8/128 - pi*a*b*x**8/64 - 3*pi*a**2*x**8/128 + O(x**9)],
    [                                                                        0, pi*x**4/4,                                                      O(x**6),                                                                         O(x**8)],
    [                                      pi*b*x**4/8 + pi*a*x**4/8 + O(x**5),   O(x**6), pi*b**2*x**6/32 + pi*a*b*x**6/48 + pi*a**2*x**6/32 + O(x**7),                                           pi*b*x**6/12 + pi*a*x**6/12 + O(x**7)],
    [                                                               -pi*x**2/2,         0,                       -pi*b*x**4/16 - pi*a*x**4/16 + O(x**5),       -pi*x**4/4 - pi*b**2*x**6/64 - pi*a*b*x**6/96 - pi*a**2*x**6/64 + O(x**7)]])

    C2 = Matrix(4, 4, lambda i, j: Add(*(A[i,k]*B[k,j] for k in range(4))))

    assert A*B == C == C2

