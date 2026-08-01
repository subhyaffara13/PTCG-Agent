
def test_representing_matrices():
    R, x,y = ring("x,y", QQ, grlex)

    basis = [(0, 0), (0, 1), (1, 0), (1, 1)]
    F = [x**2 - x - 3*y + 1, -2*x + y**2 + y - 1]

    assert _representing_matrices(basis, F, R) == [
        [[QQ(0, 1), QQ(0, 1),-QQ(1, 1), QQ(3, 1)],
         [QQ(0, 1), QQ(0, 1), QQ(3, 1),-QQ(4, 1)],
         [QQ(1, 1), QQ(0, 1), QQ(1, 1), QQ(6, 1)],
         [QQ(0, 1), QQ(1, 1), QQ(0, 1), QQ(1, 1)]],
        [[QQ(0, 1), QQ(1, 1), QQ(0, 1),-QQ(2, 1)],
         [QQ(1, 1),-QQ(1, 1), QQ(0, 1), QQ(6, 1)],
         [QQ(0, 1), QQ(2, 1), QQ(0, 1), QQ(3, 1)],
         [QQ(0, 1), QQ(0, 1), QQ(1, 1),-QQ(1, 1)]]]

