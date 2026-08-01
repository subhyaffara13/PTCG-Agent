
def test_cramer_solve(det_method, M, rhs):
    assert simplify(M.cramer_solve(rhs, det_method=det_method) - M.LUsolve(rhs)
                    ) == Matrix.zeros(M.rows, rhs.cols)

