
def unfold(
    input: Tensor,
    kernel_size: BroadcastingList2[int],
    dilation: BroadcastingList2[int] = 1,
    padding: BroadcastingList2[int] = 0,
    stride: BroadcastingList2[int] = 1,
) -> Tensor:
    r"""Extract sliding local blocks from a batched input tensor.

    .. warning::
        Currently, only 4-D input tensors (batched image-like tensors) are
        supported.

    .. warning::

        More than one element of the unfolded tensor may refer to a single
        memory location. As a result, in-place operations (especially ones that
        are vectorized) may result in incorrect behavior. If you need to write
        to the tensor, please clone it first.


    See :class:`torch.nn.Unfold` for details
    """
    if has_torch_function_unary(input):
        return handle_torch_function(
            unfold,
            (input,),
            input,
            kernel_size,
            dilation=dilation,
            padding=padding,
            stride=stride,
        )
    return torch._C._nn.im2col(
        input, _pair(kernel_size), _pair(dilation), _pair(padding), _pair(stride)
    )


def unfold(x, dimension, size, step):
    sizes = x.get_size()
    ndim = len(sizes)
    dim = canonicalize_dim(ndim, dimension)

    if ndim == 0:
        return slice_(unsqueeze(x, 0), end=size, clamp=False)

    dim_size = sizes[dim]
    sizevars = V.graph.sizevars
    sizevars.check_leq(size, dim_size)
    sizevars.check_lt(0, step)  # type: ignore[arg-type]

    new_dim_size = FloorDiv(dim_size - size, step) + 1
    if sizevars.guarding_hint_or_throw(dim_size) > 0:
        x.mark_reuse(
            sizevars.guarding_hint_or_throw(CeilDiv(new_dim_size * size, dim_size))
        )

    out_size = [*sizes[:dim], new_dim_size, *sizes[dim + 1 :], size]

    def reindexer(idx):
        dim_idx = idx[-1] + idx[dim] * step
        return (*idx[:dim], dim_idx, *idx[dim + 1 : -1])

    return TensorBox(ir.GenericView.create(x, out_size, reindexer))


def unfold(
    self: TensorLikeType, dimension: int, size: int, step: int
) -> TensorLikeType:
    shape, strides = _get_unfold_shape_stride(
        self.shape, self.stride(), dimension, size, step
    )
    return self.as_strided(shape, strides)


def unfold(g: jit_utils.GraphContext, input, dimension, size, step):
    const_size = symbolic_helper._maybe_get_const(size, "i")
    const_step = symbolic_helper._maybe_get_const(step, "i")
    if not symbolic_helper._is_value(const_size) and not symbolic_helper._is_value(
        const_step
    ):
        return opset9.unfold(g, input, dimension, const_size, const_step)

    sizedim = symbolic_helper._get_tensor_dim_size(input, dimension)
    if sizedim is not None:
        low_start = g.op("Constant", value_t=torch.tensor(0))
        low_end = g.op("Constant", value_t=torch.tensor(sizedim))
        hi_end = g.op("Constant", value_t=torch.tensor(sizedim + 1))
        low_indices = g.op("Range", low_start, low_end, step)
        hi_indices = g.op("Range", size, hi_end, step)

        low_size = symbolic_helper._size_helper(
            g, low_indices, g.op("Constant", value_t=torch.tensor(0))
        )
        hi_size = symbolic_helper._size_helper(
            g, hi_indices, g.op("Constant", value_t=torch.tensor(0))
        )

        ndim = symbolic_helper._get_tensor_rank(input)
        if ndim is None:
            raise AssertionError("ndim must be non-None")
        perm = list(range(ndim))
        perm.append(perm.pop(dimension))

        unsqueeze_list = []
        loop_condition = g.op("Constant", value_t=torch.tensor(1))
        loop_condition = g.op(
            "Cast", loop_condition, to_i=_C_onnx.TensorProtoDataType.BOOL
        )
        loop_len = g.op("Min", low_size, hi_size)

        loop, (loop_context,), _ = jit_utils.add_op_with_blocks(
            g, "Loop", loop_len, loop_condition, n_blocks=1
        )

        loop_block = loop_context.block
        block_input_iter = utils._add_input_to_block(loop_block)
        cond = utils._add_input_to_block(loop_block)  # noqa: F841

        starts = loop_context.op("Gather", low_indices, block_input_iter)
        ends = loop_context.op("Gather", hi_indices, block_input_iter)
        axes = loop_context.op("Constant", value_t=torch.tensor([2]))
        starts = symbolic_helper._unsqueeze_helper(loop_context, starts, [0])
        ends = symbolic_helper._unsqueeze_helper(loop_context, ends, [0])
        stack = loop_context.op("Slice", input, starts, ends, axes)

        unsqueeze = symbolic_helper._unsqueeze_helper(
            loop_context, loop_context.op("Transpose", stack, perm_i=perm), [dimension]
        )
        unsqueeze_list.append(unsqueeze)
        concat = loop_context.op("Concat", *unsqueeze_list, axis_i=0)

        cond_out = loop_context.op(
            "Cast",
            loop_condition,
            # pyrefly: ignore [bad-argument-type]
            _C_onnx.TensorProtoDataType.BOOL,
        )
        utils._add_output_to_block(loop_block, cond_out)
        utils._add_output_to_block(loop_block, concat)

        loop_output = loop.node().output()
        perm = [0, 1, 2, 3, 4]
        perm[0], perm[dimension + 1] = perm[dimension + 1], perm[0]
        transpose = g.op("Transpose", loop_output, perm_i=perm)
        squeeze = symbolic_helper._squeeze_helper(g, transpose, [0])

        return squeeze

    return symbolic_helper._unimplemented("Unfold", "input size not accessible")


def unfold(g: jit_utils.GraphContext, input, dimension, size, step):
    sizes = symbolic_helper._get_tensor_sizes(input)
    # FIXME(justinchuby): Get rid of the try catch here to improve readability
    try:
        sizedim = sizes[dimension]
    except Exception:
        # FIXME(justinchuby): Avoid catching Exception.
        # Catch a more specific exception instead.
        sizedim = None
    if sizedim is not None:
        low_indices = range(0, sizedim, step)
        hi_indices = range(size, sizedim + 1, step)
        stack = [
            symbolic_helper._slice_helper(
                g, input, axes=[dimension], starts=[low], ends=[hi]
            )
            for low, hi in zip(low_indices, hi_indices)
        ]
        ndim = len(sizes)
        perm = list(range(ndim))
        perm.append(perm.pop(dimension))
        unsqueeze = [
            symbolic_helper._unsqueeze_helper(
                g, g.op("Transpose", t, perm_i=perm), [dimension]
            )
            for t in stack
        ]
        return g.op("Concat", *unsqueeze, axis_i=dimension)
    else:
        return symbolic_helper._unimplemented(
            "Unfold", "input size not accessible", input
        )

