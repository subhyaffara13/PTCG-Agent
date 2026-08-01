
def meta__scaled_dot_product_attention_math_for_mps(
    query: Tensor,
    key: Tensor,
    value: Tensor,
    attn_mask: Tensor | None = None,
    dropout_p: float = 0.0,
    is_causal: bool = False,
    dropout_mask: Tensor | None = None,
    scale: float | None = None,
    enable_gqa: bool = False,
) -> tuple[Tensor, Tensor]:
    def ensure_4d(x):
        if x.dim() == 3:
            return x.unsqueeze(0), True
        elif x.dim() > 4:
            batch_size = 1
            for i in range(x.dim() - 3):
                batch_size *= x.shape[i]
            return x.view(batch_size, x.size(-3), x.size(-2), x.size(-1)), True
        else:
            return x, False

    q_, unsqueezed = ensure_4d(query)
    k_, _ = ensure_4d(key)
    v_, _ = ensure_4d(value)

    batch_size, num_head, q_size, _ = q_.shape
    _, _, max_seq_length, value_head_size = v_.shape

    def sdpa_general_mps():
        out = q_.new_empty((batch_size, num_head, q_size, value_head_size))
        attn = q_.new_empty((batch_size, num_head, q_size, max_seq_length))
        if unsqueezed:
            if query.dim() == 3:
                out = out.squeeze(0)
                attn = attn.squeeze(0)
            else:
                out_shape = list(query.shape[:-3]) + list(out.shape[1:4])
                attn_shape = list(query.shape[:-3]) + list(attn.shape[1:4])
                out = out.view(out_shape)
                attn = attn.view(attn_shape)
        return out, attn

    # sdpa_vector_2pass_mps and sdpa_vector_fast_mps are intentionally left out.
    # See https://github.com/pytorch/pytorch/issues/177603 for additional context.
    return sdpa_general_mps()

