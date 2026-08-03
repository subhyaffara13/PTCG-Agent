import functools

def sample_inputs_flex_attention_backward(
    opinfo, device, dtype, requires_grad, **kwargs
):
    make_arg = functools.partial(
        make_tensor, device=device, dtype=dtype, requires_grad=False
    )

    def score_mod(score, b, h, m, n):
        return score

    def mask_mod(b, h, m, n):
        return m >= n

    q, k, v = (make_arg(2, 2, 128, 16, low=0.1, high=2) for _ in range(3))
    block_mask = create_block_mask(mask_mod, B=2, H=2, Q_LEN=128, KV_LEN=128, device=device)
    scale = 1.0 / q.size(-1) ** 0.5
    out, logsumexp, _ = flex_attention_hop(
        q, k, v, score_mod, block_mask.as_tuple(), scale, {},
    )
    yield SampleInput(
        q,
        args=(
            k, v, out.detach(), logsumexp.detach(), torch.rand_like(out), None,
            score_mod, None, block_mask.as_tuple(),
            scale, {}, (), (),
        ),
    )

