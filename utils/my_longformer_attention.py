
def my_longformer_attention(
    g,
    input,
    weight,
    bias,
    mask,
    global_weight,
    global_bias,
    global_mask,
    num_heads,
    window,
):
    return g.op(
        "com.microsoft::LongformerAttention",
        input,
        weight,
        bias,
        mask,
        global_weight,
        global_bias,
        global_mask,
        num_heads_i=num_heads,
        window_i=window,
    )

