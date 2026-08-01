
def _per_token_quant_qparam_dim_check(input, scales, zero_points):
    num_tokens = math.prod(list(input.size())[:-1])
    if num_tokens != scales.numel():
        raise AssertionError(f"num_tokens: {num_tokens} scales: {scales.size()}")
    if num_tokens != zero_points.numel():
        raise AssertionError(
            f"num_tokens: {num_tokens} zero_points: {zero_points.size()}"
        )

