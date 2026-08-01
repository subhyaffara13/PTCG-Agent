
def test_constant_system():
    A = Matrix([[-(x + 3)/(x - 1), (x + 1)/(x - 1), 1],
                [-x - 3, x + 1, x - 1],
                [2*(x + 3)/(x - 1), 0, 0]], t)
    u = Matrix([[(x + 1)/(x - 1)], [x + 1], [0]], t)
    DE = DifferentialExtension(extension={'D': [Poly(1, x)]})
    R = QQ.frac_field(x)[t]
    assert constant_system(A, u, DE) == \
        (Matrix([[1, 0, 0],
                 [0, 1, 0],
                 [0, 0, 0],
                 [0, 0, 1]], ring=R), Matrix([0, 1, 0, 0], ring=R))

