
def test_can_blas_on_healed_broadcast_dimensions() -> None:
    expr = contract_expression("ab,bc,bd->acd", (5, 4), (1, 5), (4, 20))
    # first contraction involves broadcasting
    assert expr.contraction_list[0][2] == "bc,ab->bca"
    assert expr.contraction_list[0][-1] is False
    # but then is healed GEMM is usable
    assert expr.contraction_list[1][2] == "bca,bd->acd"
    assert expr.contraction_list[1][-1] == "GEMM"

