
def meta__dyn_quant_matmul_4bit(
    inp,
    packed_weights,
    block_size,
    in_features,
    out_features,
):
    torch._check(inp.dim() == 2, lambda: "input must be a 2D tensor")
    torch._check(
        (inp.dtype == torch.float32)
        or (inp.dtype == torch.bfloat16 and block_size == in_features),
        lambda: (
            f"expected input to be f32 or bf16 (bf16 requires block_size == in_features), "
            f"got {inp.dtype} with block_size={block_size} and in_features={in_features}"
        ),
    )
    M = inp.size(0)
    return inp.new_empty(M, out_features, dtype=inp.dtype)

