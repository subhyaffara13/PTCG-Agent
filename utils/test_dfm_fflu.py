
def test_dfm_fflu(name, A, P_ans, L_ans, D_ans, U_ans):
    pytest.importorskip('flint')
    if A.domain not in (ZZ, QQ) and not A.domain.is_FF:
        pytest.skip("Domain not supported by DFM")
    A = A.to_dfm()
    _check_fflu_result(A.fflu(), A, P_ans, L_ans, D_ans, U_ans)

