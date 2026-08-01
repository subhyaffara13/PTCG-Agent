
def test_trimming_maximum(rn, cn, max_els, max_rows, max_cols, exp_rn, exp_cn):
    rn, cn = _get_trimming_maximums(
        rn, cn, max_els, max_rows, max_cols, scaling_factor=0.5
    )
    assert (rn, cn) == (exp_rn, exp_cn)

