
def test_O2():
    assert Matrix((2, 2, -3)).cross(Matrix((1, 3, 1))) == Matrix([[11],
                                                                  [-5],
                                                                  [4]])

