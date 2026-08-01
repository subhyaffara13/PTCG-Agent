
def _check_batch_size_nested(params: SDPAParams, debug=False) -> bool:
    # This is expected to be called after check_tensor_shapes ensuring that the
    # size() calls won't error since the inputs are all 4 dimensional
    q_batch_size = params.query.size(0)
    k_batch_size = params.key.size(0)
    v_batch_size = params.value.size(0)

    # num_heads logic for nested input is checked in
    # check_for_seq_len_0_nested_tensor as there is handling there to make sure
    # num_heads is not ragged
    return q_batch_size == k_batch_size and q_batch_size == v_batch_size

