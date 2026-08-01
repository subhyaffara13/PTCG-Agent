
def test_P11():
    # raises NotImplementedError("Matrix([[x,y],[1,x*y]]).inv()
    #   not simplifying to extract common factor")
    assert Matrix([[x, y],
                   [1, x*y]]).inv() == (1/(x**2 - 1))*Matrix([[x, -1],
                                                              [-1/y, x/y]])

