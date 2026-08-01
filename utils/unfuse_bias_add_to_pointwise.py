
def unfuse_bias_add_to_pointwise(match: Match, mat1, mat2, *, inp, alpha, beta):
    if config.keep_addmm_fused_for_half_dtypes and inp.meta["val"].dtype in (
        torch.bfloat16,
        torch.float16,
    ):
        return

    def repl(inp, x1, x2, alpha, beta):
        mm_result = x1 @ x2
        if alpha != 1:
            mm_result = alpha * mm_result
        if beta != 1:
            inp = beta * inp
        return inp + mm_result

    # pyrefly: ignore [bad-argument-type]
    match.replace_by_example(repl, [inp, mat1, mat2, alpha, beta])

