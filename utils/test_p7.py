
def test_P7():
    M = Matrix([[x, y]])*(
        z*Matrix([[1, 3, 5],
                  [2, 4, 6]]) + Matrix([[7, -9, 11],
                                        [-8, 10, -12]]))
    assert M == Matrix([[x*(z + 7) + y*(2*z - 8), x*(3*z - 9) + y*(4*z + 10),
                         x*(5*z + 11) + y*(6*z - 12)]])

