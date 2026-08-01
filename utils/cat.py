
def cat(fname, fallback=_DEFAULT, _open=open_text):
    """Read entire file content and return it as a string. File is
    opened in text mode. If specified, `fallback` is the value
    returned in case of error, either if the file does not exist or
    it can't be read().
    """
    if fallback is _DEFAULT:
        with _open(fname) as f:
            return f.read()
    else:
        try:
            with _open(fname) as f:
                return f.read()
        except OSError:
            return fallback


def cat(tensors: list[list[int]], dim: int):
    check_cat_no_zero_dim(tensors)
    dim = legacy_cat_wrap_dim(dim, tensors)
    if len(tensors) <= 0:
        raise AssertionError("Cannot concatenate empty list of tensors")
    not_skipped_tensor: Optional[list[int]] = None
    for tensor in tensors:
        if not should_skip(tensor):
            not_skipped_tensor = tensor
    if not_skipped_tensor is None:
        return [0]

    cat_dim_size = 0

    for i in range(len(tensors)):
        tensor = tensors[i]
        if not should_skip(tensor):
            check_cat_shape_except_dim(not_skipped_tensor, tensor, dim, i)
            cat_dim_size = cat_dim_size + tensor[dim]

    result_size = _copy(not_skipped_tensor)
    result_size[dim] = cat_dim_size
    return result_size


def cat(
    tensors: list[torch.Tensor],
    dim: int = 0,
) -> torch.Tensor:
    def non_empty_tensor(x: torch.Tensor) -> bool:
        # For better or worse, this is a valid cat:
        #
        #   torch.cat([torch.randn(2, 2, 4), torch.randn(0), torch.randn(3, 2, 4)])
        #
        # We'd like to eliminate naughtiness like this for downstream passes
        # like split_cat.  The easiest way is to just drop such inputs
        # (guarding that they are non-zero).
        #
        # Is it permissible for this filtering to be size-oblivious?  A case
        # where this could matter is cat([(2, 2), (u0,)], dim=0); if u0
        # happened to be zero, we would have liked to have filtered it out.
        # But actually, the ONLY way this could have passed is if u0 == 0,
        # so by the time we get here we have already installed a deferred
        # runtime assert forcing u0 to be zero.  So if this hasn't happened,
        # we know that the unbacked SymInt has appropriate size and there are
        # no problems.
        if len(x.shape) == 1 and guard_or_false(x.shape[0] == 0):
            return False

        if dim < len(x.shape) and guard_or_false(x.shape[dim] == 0):
            return False

        return True

    filtered_tensors = list(filter(non_empty_tensor, tensors))

    if len(filtered_tensors) == 1:
        # check dtype promotion
        promoted_dtype = elementwise_dtypes(
            *tensors,
            type_promotion_kind=ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT,
        )[1]
        filtered_t = filtered_tensors[0]
        return (
            filtered_t.clone()
            if promoted_dtype == filtered_t.dtype
            else filtered_t.to(dtype=promoted_dtype)
        )
    elif 1 < len(filtered_tensors) < len(tensors):
        # on the first call, when we remove empty tensors, we redispatch recursively
        return aten.cat.default(filtered_tensors, dim)

    # optimization, avoid concat for single, repeated input
    if len(filtered_tensors) > 1 and all(
        t is filtered_tensors[0] for t in filtered_tensors
    ):
        inp = filtered_tensors[0]
        shape = list(inp.shape)
        dim = dim + len(inp.shape) if dim < 0 else dim
        shape.insert(dim, len(filtered_tensors))
        return inp.unsqueeze(dim).expand(*shape).flatten(dim, dim + 1).clone()

    # when no 'filtering' has occurred, we raise to prevent infinite recursion (no more decomposition needed)
    return NotImplemented


def cat(inputs, dim=0):
    """Lower aten.cat, choosing between pointwise_cat and ConcatKernel."""
    cpu_device = inputs[0].get_device().type == "cpu"
    if cpu_device and all(
        input.get_dtype() in [torch.int8, torch.uint8] for input in inputs
    ):
        # TODO <leslie> Remove this fallback when we support vectorization
        # code gen with uint8 data type directly.
        for input in inputs:
            input.realize()
        if all(len(input.get_size()) == 4 for input in inputs):
            inputs, _ = require_channels_last(aten.cat, *inputs)
        return fallback_handler(aten.cat.default)(inputs, dim)

    if len(inputs) == 1:
        return clone(inputs[0])

    dim = _validate_dim(inputs[0], dim, 0)
    dtype = get_promoted_dtype(
        *inputs, type_promotion_kind=ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT
    )
    inputs = [to_dtype(inp, dtype) for inp in inputs]

    def unwrap_tensor(x: TensorBox | ir.StorageBox) -> ir.IRNode:
        if isinstance(x, TensorBox):
            if isinstance(x.data, ir.BaseView):
                return x.data.unwrap_view()
            else:
                return x.data

        if isinstance(x, ir.StorageBox):
            return x.data

        return x

    def is_reduction(t):
        return isinstance(t, ir.ComputedBuffer) and isinstance(t.data, ir.Reduction)

    def can_fuse_reduction(t):
        if isinstance(t, (TensorBox, ir.StorageBox)):
            return can_fuse_reduction(unwrap_tensor(t))
        return (
            is_reduction(t)
            or isinstance(t, ir.Pointwise)
            and any(
                can_fuse_reduction(V.graph.get_buffer(read))
                for read in t.get_read_names()
            )
        )

    # fusing reducutions into computed concat buffer can cause regressions.
    fusable_reduction = any(can_fuse_reduction(t) for t in inputs)

    def should_lower_cat_input(x) -> bool:
        # Unrealized inputs will not be storage and layouts, and we dont want to realize
        # them in case we want to fuse
        if ir.is_storage_and_layout(x):
            storage, _ = ir.as_storage_and_layout(x, freeze=False)
            return not ir.ConcatKernel.can_realize_into_without_copy(storage)

        if isinstance(x, (TensorBox, ir.StorageBox)):
            return should_lower_cat_input(unwrap_tensor(x))

        if isinstance(x, ir.Pointwise):
            return True

        return False

    if config.force_pointwise_cat:
        return pointwise_cat(inputs, dim)

    # TODO: We observed negative performance impact of pointwise_cat optimization on CPU so disabled it.
    #             We will revisit this later after enabling vectorization on index_expr.
    if cpu_device:
        return TensorBox(ir.ConcatKernel.create(inputs, dim))

    def op_count(x):
        if isinstance(x, (TensorBox, ir.StorageBox)):
            return op_count(unwrap_tensor(x))

        # this will correspond to a direct memory read
        if not isinstance(x, ir.Pointwise):
            return 0

        count = x.inner_fn_opcount().num_ops
        for read in x.get_read_names():
            count += op_count(V.graph.get_buffer(read))

        return count

    # as of inputs increase, possibility for register spilling also increases
    # past a certain threshold of inputs we only fuse if the if the input kernels
    # are simple
    # not sure if we want to expose to users via config since logic may change in future
    MAX_COMPLEX_POINTWISE_CAT = 8
    MAX_SIMPLE_OP_COUNT = 2

    def additional_pointwise_ops(op: torch._ops.OpOverload):
        return op in (aten.cat.default, aten.constant_pad_nd.default)

    if len(inputs) <= MAX_COMPLEX_POINTWISE_CAT or (
        (len(inputs) <= config.max_pointwise_cat_inputs)
        and all(op_count(t) <= MAX_SIMPLE_OP_COUNT for t in inputs)
    ):
        pointwise_uses = all(
            is_pointwise_use(use, additional_pointwise_ops)
            for use in V.current_node.users
        )
        # fuse in case we will be used in a pointwise node, and there are any inputs we
        # we can prevent materialization of.
        fuse_pointwise_use = (
            any(should_lower_cat_input(inp) for inp in inputs) and pointwise_uses
        )

        # horizontal fuse in case all inputs will require a copy kernel anyway.
        # only horizontally fuse pointwise kernels

        # Skip pointwise_cat when any cat input has a fusible (pointwise)
        # multi-consumer — ConcatKernel + NonOwningLayout avoids redundant
        # reads. Also skip when input is an unrealized Pointwise with
        # multiple consumers to avoid recomputation (e.g. pad-as-cat).
        def any_input_has_multi_consumers() -> bool:
            current_node = V.current_node
            if current_node is None:
                return False
            fx_args = current_node.args[0]
            if isinstance(fx_args, (list, tuple)):
                input_nodes = fx_args
            elif isinstance(fx_args, torch.fx.Node):
                input_nodes = [fx_args]
            else:
                return False

            def is_unrealized_pointwise(x):
                if isinstance(x, (TensorBox, ir.StorageBox)):
                    return is_unrealized_pointwise(unwrap_tensor(x))
                return isinstance(x, ir.Pointwise)

            for arg, ir_input in zip(input_nodes, inputs):
                if not hasattr(arg, "users") or len(arg.users) <= 1:
                    continue
                # input will be computed multiple times because other consumers
                # (eg. pointwise) will also inline it. So we should realize-in-place via ConcatKernel
                if any(is_pointwise_use(u) for u in arg.users if u is not current_node):
                    return True
                # If input is an unrealized Pointwise with multiple consumers, pointwise_cat
                # will inline input without realizing it to memory, causing separate
                # realization cost for input. So we should realize-in-place via ConcatKernel
                if is_unrealized_pointwise(ir_input):
                    return True
            return False

        has_multi_consumers = any_input_has_multi_consumers()

        horizontal_fuse_cat = all(
            should_lower_cat_input(inp) for inp in inputs
        ) and not any(can_fuse_reduction(t) for t in inputs)
        if not has_multi_consumers and (
            fuse_pointwise_use or (horizontal_fuse_cat and not fusable_reduction)
        ):
            return pointwise_cat(inputs, dim)

    return TensorBox(ir.ConcatKernel.create(inputs, dim))


def cat(tensors: TensorSequenceType, dim: int = 0) -> TensorLikeType:
    def cat_compute_output_memory_format(inputs):
        format = None
        for t in inputs:
            f = utils.suggest_memory_format(t)
            if f == torch.contiguous_format:
                return f
            if format is not None and format != f:
                return torch.contiguous_format
            format = f
        if format is None:
            raise AssertionError("format should not be None if len(inputs) > 0")
        return format

    if len(tensors) == 0:
        msg = "cat expects at least one tensor, but received zero!"
        raise ValueError(msg)

    for tensor in tensors:
        if not isinstance(tensor, TensorLike):
            raise AssertionError(f"tensor must be TensorLike, got {type(tensor)}")

    utils.check_same_device(*tensors, allow_cpu_scalar_tensors=False)

    from torch.fx.experimental.symbolic_shapes import guard_or_false

    # This is a bit tricky.  Naively, you would expect to just pick one
    # arbitrary tensor and check that all tensors match this tensor.  However,
    # there is legacy behavior which says that if you have a 1-D empty tensor
    # (0,), this is permissible.  So you can't assume that all the tensors
    # have same dimensionality, and you can't assume that the first tensor is
    # the correct stencil.
    #
    # We'll implement this in a few passes.  First, we will try to infer the
    # ndim of the cat output.  If this ndim != 1, then we know that all ndim =
    # 1 inputs must be empty, or are errors.  If this ndim == 1, then life
    # is easy (the legacy special case coincides with regular handling).
    #
    # NB: The regular implementation of cat just filters out empty inputs,
    # but we do it slightly different here for better handling for unbacked
    # SymInts

    example = None
    # pyrefly: ignore [bad-assignment]
    for i, t in enumerate(tensors):
        if example is None:
            if t.ndim != 1:
                example = t
        else:
            if t.ndim != 1:
                torch._check(
                    t.ndim == example.ndim,
                    lambda: "Number of dimensions of tensors must match.  "
                    f"Expected {example.ndim}-D tensors, but got {t.ndim}-D for "
                    f"tensor number {i} in the list",
                )

    if example is None:
        # example is None if everything is 1-D.  If so, just arbitrarily pick
        # the first one
        example = tensors[0]

    shape = example.shape
    filtered = []
    for tensor_idx, tensor in enumerate(tensors):
        if len(shape) != len(tensor.shape):
            if tensor.ndim != 1:
                raise AssertionError(
                    f"tensor.ndim should be 1 at this point, got {tensor.ndim}"
                )
            # Don't suggest the legacy behavior in the error message
            torch._check(
                # NB: it is not enough to simply assert that tensor.shape[0] == 0;
                # this MUST be true even under guard size oblivious.
                # Effectively, we must actually know that the shape is zero,
                # passing an unbacked SymInt which we will defer a runtime
                # assert on won't cut it.  This is a policy decision (size
                # oblivious semantics say that u0 tensors never are inferred
                # to be zero size, even if they must be that for the cat to go
                # through), and is load bearing for our Inductor lowerings
                # (which assume that size oblivious tests are OK to determine
                # if a shape is permissibly zero.)
                guard_or_false(tensor.shape[0] == 0),
                lambda: f"Number of dimensions of tensors must match.  "
                f"Expected {example.ndim}-D tensors, but got 1-D for "
                f"tensor number {tensor_idx} in the list",
            )
        else:
            # Remove inputs that are 1-D, zero size
            if tensor.ndim == 1 and guard_or_false(tensor.shape[0] == 0):
                continue
            # Don't bother checking size match, prims.cat will handle it
            filtered.append(tensor)

    memory_format = cat_compute_output_memory_format(tensors)

    if len(filtered) == 0:
        t = tensors[0]

        # TODO: fix this to work with meta tensors
        try:
            # BUG? This looks like it wants to call builtins.any() but is
            # actually calling .any() (in this file). Changing to builtins.any()
            # causes tests to fail:
            # PYTORCH_OPINFO_SAMPLE_INPUT_INDEX=4 python test/test_ops.py -k \
            #   TestFakeTensorCUDA.test_fake_crossref_backward_amp_cat_cuda_float32
            requires_grad = bool(any(x.requires_grad for x in tensors))  # type: ignore[arg-type]
        except Exception:
            requires_grad = False  # type: ignore[assignment]

        return empty(
            (0,),
            dtype=t.dtype,
            device=t.device,
            requires_grad=requires_grad,
            memory_format=memory_format,
        )

    dim = utils.canonicalize_dim(filtered[0].ndim, dim)
    utils.validate_idx(filtered[0].ndim, dim)

    return prims.cat(filtered, dim).clone(memory_format=memory_format)


def cat(g: jit_utils.GraphContext, tensor_list, dim):
    if symbolic_helper._is_packed_list(tensor_list):
        return opset9.cat(g, tensor_list, dim)
    else:
        dim = symbolic_helper._get_const(dim, "i", "dim")
        return g.op("ConcatFromSequence", tensor_list, axis_i=dim)


def cat(g: jit_utils.GraphContext, tensor_list, dim):
    """Implement concatenation of pytorch tensors in ONNX along the specified `dim` dimension.

    Parameters:
        g (jit_utils.GraphContext): Graph context.
        tensor_list (List[torch.Tensor]): List of tensors to concatenate.
        dim (int): Dimension along which to concatenate the tensors.

    Returns:
        ONNX graph node representing the concatenated tensor.
    """
    tensors = symbolic_helper._unpack_list(tensor_list)
    # torch.cat ignores empty tensors such as `torch.Tensor([])`
    # These needs to be removed as input from ONNX's concat too, otherwise shape inference
    # will likely fail due to inputs with different ranks (0 for empty tensor, > 0 for anything else)
    nonempty_tensors = []
    for t in tensors:
        if symbolic_helper._is_constant(t) and not symbolic_helper._get_tensor_dim_size(
            t, 0
        ):
            continue
        nonempty_tensors.append(t)
    if len(nonempty_tensors) == 0:
        raise AssertionError("nonempty_tensors must not be empty")
    if not all(
        symbolic_helper._get_tensor_rank(nonempty_tensors[0]) is None
        or symbolic_helper._get_tensor_rank(t) is None
        or symbolic_helper._get_tensor_rank(t)
        == symbolic_helper._get_tensor_rank(nonempty_tensors[0])
        for t in nonempty_tensors
    ):
        raise AssertionError("All tensors must have the same rank")
    tensor_list.node().removeAllInputs()
    for t in nonempty_tensors:
        tensor_list.node().addInput(t)

    tensors = symbolic_helper._unpack_list(tensor_list)
    return g.op("Concat", *tensors, axis_i=dim)


def cat(result: _ods_ir.Type, lhs: _ods_ir.Value[_ods_ir.RankedTensorType], rhs: _ods_ir.Value[_ods_ir.RankedTensorType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return CatOp(result=result, lhs=lhs, rhs=rhs, loc=loc, ip=ip).result


def cat(tensors: Any, dim: Any, new_dim: Any) -> _Tensor:
    n = dims(1)  # Get single Dim instead of tuple
    return stack(tensors, n, dim).index([n, dim], new_dim)  # type: ignore[list-item]

