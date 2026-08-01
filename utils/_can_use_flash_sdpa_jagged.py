
def _can_use_flash_sdpa_jagged(params: SDPAParams, debug=False) -> bool:
    constraints = (
        _check_batch_size_nested,
        _check_head_dim_size_flash_nested,
        _check_for_seq_len_0_nested,
    )
    for constraint in constraints:
        if not constraint(params, debug):
            return False
    return True

