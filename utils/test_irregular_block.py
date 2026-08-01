
def test_irregular_block():
    assert Matrix.irregular(3, ones(2,1), ones(3,3)*2, ones(2,2)*3,
        ones(1,1)*4, ones(2,2)*5, ones(1,2)*6, ones(1,2)*7) == Matrix([
        [1, 2, 2, 2, 3, 3],
        [1, 2, 2, 2, 3, 3],
        [4, 2, 2, 2, 5, 5],
        [6, 6, 7, 7, 5, 5]])


def test_irregular_block():
    assert Matrix.irregular(3, ones(2,1), ones(3,3)*2, ones(2,2)*3,
        ones(1,1)*4, ones(2,2)*5, ones(1,2)*6, ones(1,2)*7) == Matrix([
        [1, 2, 2, 2, 3, 3],
        [1, 2, 2, 2, 3, 3],
        [4, 2, 2, 2, 5, 5],
        [6, 6, 7, 7, 5, 5]])

