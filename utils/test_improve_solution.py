
def test_improve_solution():
    A = randmatrix(5, min=1e-20, max=1e20)
    b = randmatrix(5, 1, min=-1000, max=1000)
    x1 = lu_solve(A, b) + randmatrix(5, 1, min=-1e-5, max=1.e-5)
    x2 = improve_solution(A, x1, b)
    assert norm(residual(A, x2, b), 2) < norm(residual(A, x1, b), 2)

