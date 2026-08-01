
def sample_inputs_flex_attention(opinfo, device, dtype, requires_grad, **kwargs):
    make_arg = functools.partial(
        make_tensor, device=device, dtype=dtype, requires_grad=requires_grad
    )

    def score_mod(score, b, h, m, n):
        return score + h

    q, k, v = (make_arg(2, 2, 128, 8, low=0.1, high=2) for _ in range(3))
    block_mask = _create_empty_block_mask(q, k)
    yield SampleInput(q, k, v, score_mod, block_mask)

