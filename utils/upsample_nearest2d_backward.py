
def upsample_nearest2d_backward(
    grad_output: Tensor,
    output_size: Sequence[int | torch.SymInt],
    input_size: Sequence[int | torch.SymInt],
    scales_h: float | None = None,
    scales_w: float | None = None,
):
    full_output_size = upsample_common_check(
        input_size, output_size, num_spatial_dims=2
    )
    torch._check(
        grad_output.ndim == 4,
        lambda: f"Expected grad_output to be a tensor of dimension 4 but got: dimension {grad_output.ndim}",
    )
    for i in range(4):
        torch._check(
            grad_output.size(i) == full_output_size[i],
            lambda: (
                f"Expected grad_output to have the same shape as output;"
                f" output.size({i}) = {full_output_size[i]}"
                f" but got grad_output.size({i}) = {grad_output.size(i)}"
            ),
        )

    return grad_output.new_empty(input_size).to(
        memory_format=utils.suggest_memory_format(grad_output)
    )  # type: ignore[call-overload]


def upsample_nearest2d_backward(
    x, output_size=None, input_size=None, scales_h=None, scales_w=None
):
    x.realize_hint()

    *_batch, inp_h, inp_w = x.get_size()
    inp_h = V.graph.sizevars.guard_int(inp_h)
    inp_w = V.graph.sizevars.guard_int(inp_w)

    # pyrefly: ignore [not-iterable]
    *_batch, out_h, out_w = input_size

    if inp_h % out_h == 0 and inp_w % out_w == 0:
        return avg_pool2d(
            x, [FloorDiv(inp_h, out_h), FloorDiv(inp_w, out_w)], divisor_override=1
        )

    h_kernel_max = ceildiv(inp_h, out_h)
    w_kernel_max = ceildiv(inp_w, out_w)

    def start_index(index, out_dim, inp_dim):
        return CeilDiv(index * inp_dim, sympy.sympify(out_dim))

    def end_index(index, out_dim, inp_dim):
        return start_index((index + 1), out_dim, inp_dim)

    fn_sum = _adaptive_pooling_fn(
        start_index=start_index,
        end_index=end_index,
        kernel_maxes=[h_kernel_max, w_kernel_max],
        in_sizes=[inp_h, inp_w],
        out_sizes=[out_h, out_w],
        pooling_fn=ops.add,
    )

    def fn(idx):
        return fn_sum(idx, pad_adaptive_loader(x))

    rv = Pointwise.create(
        device=x.get_device(),
        dtype=x.get_dtype(),
        inner_fn=fn,
        # pyrefly: ignore [bad-argument-type, no-matching-overload]
        ranges=list(input_size),
    )

    return rv

