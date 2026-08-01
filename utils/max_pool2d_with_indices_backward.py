
def max_pool2d_with_indices_backward(
    grad_output: Tensor,
    self: Tensor,
    kernel_size,
    stride,
    padding,
    dilation,
    ceil_mode: bool,
    indices: Tensor,
):
    """
    Decomposition of max_pool2d_with_indices_backward using scatter_add.

    This replaces the native implementation with a high-level decomposition
    that uses scatter_add for gradient accumulation. The scatter-based approach
    provides automatic optimization opportunities for Inductor and handles all
    pooling configurations without requiring specialized fallback paths.

    Algorithm:
        For each output gradient position, use the corresponding index from the
        forward pass to scatter the gradient to the input position. When multiple
        output positions select the same input position as max, scatter_add
        automatically accumulates their gradients.

    Complexity: O(B * C * H_out * W_out)
        Independent of kernel size, unlike traditional O(B * C * H_in * W_in * K²)
        approaches that iterate over input positions and kernel windows.

    Known Limitations:
        - FP16/BF16: Uses FP32 accumulation internally to preserve precision when
          many gradients accumulate to the same position (overlapping pooling windows).
          This adds slight overhead but ensures numerical stability.
        - Deterministic mode: Falls back to native implementation to ensure
          consistent results across runs

    Args:
        grad_output: Gradient w.r.t. pooling output [B, C, H_out, W_out]
        self: Original input tensor (for shape) [B, C, H_in, W_in]
        kernel_size: Pooling kernel size
        stride: Pooling stride
        padding: Pooling padding
        dilation: Pooling dilation
        ceil_mode: Whether to use ceil for output size calculation
        indices: Indices from forward pass (per-channel linear positions)

    Returns:
        Gradient w.r.t. input [B, C, H_in, W_in]
    """
    # Use native kernel in deterministic mode
    if torch.are_deterministic_algorithms_enabled():
        return NotImplemented

    # MPS: Use native kernel. scatter_add has correctness issues on macOS 14
    # (#163327) and numerical differences on macOS 15+.
    if grad_output.device.type == "mps":
        return NotImplemented

    # Get spatial dimensions
    in_height = self.size(-2)
    in_width = self.size(-1)
    out_height = grad_output.size(-2)
    out_width = grad_output.size(-1)

    # Handle both 3D (C, H, W) and 4D (B, C, H, W) cases by treating 3D as 4D
    is_batched = self.dim() == 4
    if not is_batched:
        self = self.unsqueeze(0)
        grad_output = grad_output.unsqueeze(0)
        indices = indices.unsqueeze(0)

    batch_size = self.size(0)
    channels = self.size(1)

    # For FP16/BF16, use FP32 accumulation to avoid precision loss
    # This is critical when many gradients accumulate to the same position
    # (overlapping pooling windows with large kernels or stride < kernel_size)
    use_fp32_accum = grad_output.dtype in (torch.float16, torch.bfloat16)
    accum_dtype = torch.float32 if use_fp32_accum else grad_output.dtype

    # Create grad_input with correct accumulation dtype from the start
    grad_input_flat = torch.zeros(
        batch_size * channels,
        in_height * in_width,
        dtype=accum_dtype,
        device=grad_output.device,
    )

    # Reshape grad_output and indices to (B*C, H_out*W_out)
    grad_output_flat = grad_output.reshape(
        batch_size * channels, out_height * out_width
    )
    indices_flat = indices.reshape(batch_size * channels, out_height * out_width)

    # Convert grad_output to accumulation dtype if needed
    if use_fp32_accum:
        grad_output_flat = grad_output_flat.to(torch.float32)

    # Scatter gradients to input positions
    grad_input_flat = grad_input_flat.scatter_add(1, indices_flat, grad_output_flat)

    # Reshape back to original input shape
    grad_input = grad_input_flat.reshape(batch_size, channels, in_height, in_width)

    # Convert back to original dtype if we used FP32 accumulation
    if use_fp32_accum:
        grad_input = grad_input.to(grad_output.dtype)

    # Preserve memory format from input (channels_last vs channels_first)
    memory_format = utils.suggest_memory_format(self)
    grad_input = grad_input.contiguous(memory_format=memory_format)

    # Remove batch dimension for 3D case
    if not is_batched:
        grad_input = grad_input.squeeze(0)

    return grad_input


def max_pool2d_with_indices_backward(
    grad_output, x, kernel_size, stride, padding, dilation, ceil_mode, indices
):
    if padding == 0:
        padding = [0, 0]
    if dilation == 1:
        dilation = [1, 1]
    if not stride:
        stride = kernel_size

    assert isinstance(x, TensorBox)
    assert len(kernel_size) == 2
    assert len(stride) == 2
    assert len(padding) == 2
    assert len(dilation) == 2
    assert len(x.get_size()) in (3, 4)

    # we will read this many times, so make sure it is computed
    grad_output.realize_hint()
    gO_stride = grad_output.maybe_get_stride()
    x_stride: Sequence[Any] | None
    if isinstance(x, TensorBox) and isinstance(x.data.data, Pointwise):  # type: ignore[attr-defined]
        data = x.data.data  # type: ignore[attr-defined]
        device = data.get_device()
        assert device is not None
        x_buffer = ir.ComputedBuffer(
            name=None,
            layout=ir.FlexibleLayout(
                device=device,
                dtype=data.get_dtype(),
                size=data.get_size(),
            ),
            data=data,
        )
        x_buffer.decide_layout()
        x_stride = x_buffer.get_stride()
    else:
        x_stride = x.maybe_get_stride()

    is_channels_last = (x_stride is not None and x_stride[1] == 1) or (
        gO_stride is not None and gO_stride[1] == 1
    )
    if any(d != 1 for d in dilation):
        # dilation NYI
        return fallback_max_pool2d_with_indices_backward(
            grad_output, x, kernel_size, stride, padding, dilation, ceil_mode, indices
        )

    *_batch, _height, width = x.get_size()
    *_, pooled_height, pooled_width = grad_output.get_size()

    indices_loader = indices.make_loader()
    grad_loader = grad_output.make_loader()
    new_size = list(x.get_size())

    h_window_size = max(
        max(FloorDiv(h, stride[0]) - max(0, FloorDiv(h - kernel_size[0], stride[0])), 1)
        for h in range(kernel_size[0] * 2)
    )
    w_window_size = max(
        max(FloorDiv(w, stride[1]) - max(0, FloorDiv(w - kernel_size[1], stride[1])), 1)
        for w in range(kernel_size[1] * 2)
    )

    window_size = h_window_size * w_window_size

    if window_size > 25:
        # Kernel size too big. Results in hard-to-optimize Triton code. Use fallback.
        return fallback_max_pool2d_with_indices_backward(
            grad_output, x, kernel_size, stride, padding, dilation, ceil_mode, indices
        )

    indices_size = indices.get_size()

    def fn(idx):
        *prefix, h, w = idx
        index_test = ops.index_expr(h * width + w, torch.int32)
        h = h + padding[0]
        w = w + padding[1]
        phstart = ops.index_expr(
            FloorDiv(h - kernel_size[0] + stride[0], stride[0]), torch.int32
        )
        pwstart = ops.index_expr(
            FloorDiv(w - kernel_size[1] + stride[1], stride[1]), torch.int32
        )
        phend = ops.index_expr(FloorDiv(h, stride[0]) + 1, torch.int32)
        pwend = ops.index_expr(FloorDiv(w, stride[1]) + 1, torch.int32)

        phstart = ops.maximum(phstart, ops.constant(0, torch.int32))
        pwstart = ops.maximum(pwstart, ops.constant(0, torch.int32))
        phend = ops.minimum(phend, ops.index_expr(pooled_height, torch.int32))
        pwend = ops.minimum(pwend, ops.index_expr(pooled_width, torch.int32))

        gradient = None
        for ph_ in range(h_window_size):
            for pw_ in range(w_window_size):
                ph = ops.add(phstart, ops.constant(ph_, torch.int32))
                pw = ops.add(pwstart, ops.constant(pw_, torch.int32))
                grad_index = [
                    *prefix,
                    ops.indirect_indexing(
                        ops.minimum(ph, ops.sub(phend, ops.constant(1, torch.int32))),
                        indices_size[-2],
                        check=False,
                    ),
                    ops.indirect_indexing(
                        ops.minimum(pw, ops.sub(pwend, ops.constant(1, torch.int32))),
                        indices_size[-1],
                        check=False,
                    ),
                ]

                index_actual = indices_loader(grad_index)
                grad_part = grad_loader(grad_index)
                check = ops.eq(index_actual, index_test)

                if gradient is None:
                    # don't need mask for 0, 0
                    gradient = ops.where(
                        check, grad_part, ops.constant(0.0, torch.float32)
                    )
                else:
                    mask = ops.and_(
                        ops.and_(
                            ops.lt(ph, phend),
                            ops.lt(pw, pwend),
                        ),
                        check,
                    )
                    gradient = ops.where(mask, ops.add(gradient, grad_part), gradient)
        assert gradient is not None
        return gradient

    out = Pointwise.create(
        device=grad_output.get_device(),
        dtype=grad_output.get_dtype(),
        inner_fn=fn,
        ranges=new_size,
    )
    if is_channels_last:
        return ir.ExternKernel.require_channels_last(out)
    else:
        return out

