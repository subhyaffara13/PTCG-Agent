
def test_ddm_fflu(name, A, P_ans, L_ans, D_ans, U_ans):
    A = A.to_ddm()
    _check_fflu_result(A.fflu(), A, P_ans, L_ans, D_ans, U_ans)

