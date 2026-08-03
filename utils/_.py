import itertools
import pathlib
import re
from typing import Any, Tuple, Union

def _(eps):
    r"""
    >>> ep, = load('[console_scripts]\nfoo=bar')
    >>> ep.group
    'console_scripts'
    >>> ep.name
    'foo'
    >>> ep.value
    'bar'
    """
    return validate(metadata.EntryPoints(metadata.EntryPoints._from_text(eps)))


def _(lib: Library, schema, alias_analysis=""):
    """The old torch.library.define.
    We're keeping this around for BC reasons
    """

    def wrap(f):
        name = lib.define(schema, alias_analysis)
        lib.impl(name, f)
        return f

    return wrap


def _(input: torch.Tensor) -> torch.Tensor:
    """
    Meta kernel for _wrap_tensor_autograd.
    """
    return torch.empty_like(input)


def _(
    shape: list[int],
    indices: list[Tensor],
    vals: Tensor,
) -> Tensor:
    return vals.new_empty(shape)


def _(info, indims, shape, indices, value):  # type: ignore[no-untyped-def]
    """The batching rule is special in that it returns a tensor that is not batched"""
    indices_indims = indims[1]
    expanded_indices = []
    for idx, idx_indim in zip(indices, indices_indims):
        # The index is not a being batched, we should unsqueeze and expand to val
        if idx_indim is None:
            expanded_indices.append(idx.expand(value.shape))
        else:
            # the index is being part of the vmap batch, it should be the same size as val
            assert idx.shape == value.shape
            expanded_indices.append(idx)

    out = torch.ops.flex_lib.zeros_and_scatter(
        shape,
        expanded_indices,
        value,
    )
    return out, None


def _(*inputs, asm_str, constraints, dtype, is_pure=True, pack=1):
    return _inline_asm_dense(
        *inputs,
        asm_str=asm_str,
        constraints=constraints,
        dtype=dtype,
        is_pure=is_pure,
        pack=pack,
    )


def _(mode, *inputs, asm_str, constraints, dtype, is_pure=True, pack=1):
    with mode:
        return _elementwise_output_like(*inputs, dtype=dtype)


def _(mode, *inputs, asm_str, constraints, dtype, is_pure=True, pack=1):
    proxy_args = pytree.tree_map(mode.tracer.unwrap_proxy, inputs)

    out_proxy = mode.tracer.create_proxy(
        "call_function",
        inline_asm_elementwise,
        proxy_args,
        {
            "asm_str": asm_str,
            "constraints": constraints,
            "dtype": dtype,
            "is_pure": is_pure,
            "pack": pack,
        },
        name="inline_asm_elementwise",
    )

    out = inline_asm_elementwise(
        *inputs,
        asm_str=asm_str,
        constraints=constraints,
        dtype=dtype,
        is_pure=is_pure,
        pack=pack,
    )
    return track_tensor_tree(out, out_proxy, constant=None, tracer=mode.tracer)


def _(ctx, *inputs, asm_str, constraints, dtype, is_pure=True, pack=1):
    unwrapped_inputs = ctx.unwrap_tensors(inputs)

    with ctx.redispatch_to_next():
        res = inline_asm_elementwise(
            *unwrapped_inputs,
            asm_str=asm_str,
            constraints=constraints,
            dtype=dtype,
            pack=pack,
        )
    return ctx.wrap_tensors(res)


def _(subgraph, identifier, *operands):
    # Check if we have already traced the subgraph.
    invoke_subgraph_cache = get_invoke_subgraph_cache()
    if invoke_subgraph_cache:
        if saved_autograd_fn := invoke_subgraph_cache.get_autograd_key_entry(
            identifier
        ):
            return saved_autograd_fn(*operands)

    output_metadata = get_output_metadata(subgraph, *operands)

    def autograd_fn_callable(*args):
        return InvokeSubgraphAutogradOp.apply(
            subgraph, identifier, output_metadata, *args
        )

    # Save the autograd_fn_callable in the dispatch set cache.
    if invoke_subgraph_cache:
        invoke_subgraph_cache.add_autograd_key_entry(identifier, autograd_fn_callable)

    return autograd_fn_callable(*operands)


def _(debug_mode, subgraph, identifier, *operands):
    # record HOP call
    call = torch.utils._debug_mode._OpCall(
        invoke_subgraph,
        (identifier, *operands),
        kwargs={},
        call_depth=debug_mode.call_depth + 1,
        stack=debug_mode.record_stack_trace,
    )
    debug_mode._record_call(call)

    debug_mode.call_depth += 1
    debug_mode._handle_annotate(f"[enter InvokeSubgraph HOP] {identifier}")

    # If the HOP is dispatched from DebugMode, we should enable debug_mode
    # for the subgraph call.
    with debug_mode:
        if getattr(subgraph, "_boxed_call", False):
            result = subgraph(list(operands))
        else:
            result = subgraph(*operands)
    debug_mode._handle_annotate(f"[exit InvokeSubgraph HOP] {identifier}")
    debug_mode.call_depth -= 1
    # record output of HOP
    debug_mode._record_call_output(call, result)
    return result


def _(subgraph, identifier, *operands):
    from torch.utils._python_dispatch import _get_current_dispatch_mode

    mode = _get_current_dispatch_mode()

    if mode is not None:
        raise AssertionError("Mode should never be enabled for CPU/CUDA key")

    if getattr(subgraph, "_boxed_call", False):
        return subgraph(list(operands))
    else:
        return subgraph(*operands)


def _(ctx, subgraph, identifier, *operands):
    from torch._higher_order_ops.auto_functionalize import (
        can_auto_functionalize,
        do_auto_functionalize_v2,
    )

    # (in the functionalization metadata phase) Capture tokens before
    tokens_before = dict(ctx.mode._tokens)

    # Check if this subgraph has effects stored in the cache
    invoke_subgraph_cache = get_invoke_subgraph_cache()
    effects = None
    if invoke_subgraph_cache:
        effects = invoke_subgraph_cache.get_effects(identifier)

    if effects:
        if len(effects) != 1:
            raise AssertionError(
                f"Multiple effects within a subgraph NYI, got {len(effects)} effects"
            )
        tokens = ctx.mode._tokens
        effects = next(iter(effects))
        token_input = tokens[effects]

        operands = (token_input, *operands)

        def wrap_subgraph(subgraph):
            def wrapped_subgraph(token, *args):
                res = subgraph(*args)
                return ctx.unwrap_tensors(ctx.mode._tokens[effects]), *res

            return wrapped_subgraph

        subgraph = wrap_subgraph(subgraph)

    unwrapped_operands = ctx.unwrap_tensors(operands)

    hop_instance = HopInstance.create(invoke_subgraph, subgraph, identifier, *operands)
    if can_auto_functionalize(hop_instance):
        # NOTE: [auto_functionalize x invoke_subgraph caching]
        # We call auto_functionalized_v2 to support input mutation of invoke_subgraph.
        # See NOTE [Support input mutation of hops] for the overall design.
        #
        # invoke_subgraph is special because of its identifier based caching mechanism.
        # In invoke_subgraph's functionalization key implementation, we create a new
        # identifier because the subgraph is replaced by FunctionWithNoFreeVars in a
        # functional + epilogue form.
        if not isinstance(identifier, str):
            raise AssertionError(
                f"identifier must be a string for auto_functionalize, got {type(identifier)}"
            )
        return do_auto_functionalize_v2(
            ctx.mode,
            hop_instance,
            (subgraph, "auto_functionalized_" + identifier, *operands),
            {},
        )

    with ctx.redispatch_to_next():
        # NB: There is an assumption that subgraph does not mutate inputs and
        # there is no aliasing. It's Dynamo's responsibility to prevent formation
        # of invoke_subgraph ops if input aliasing/mutation is detected.
        functionalized_subgraph = FunctionalizeCtxWrapper(ctx, subgraph)
        out = invoke_subgraph(functionalized_subgraph, identifier, *unwrapped_operands)

    if effects:
        (new_token, *out) = out
        ctx.mode._tokens[effects] = new_token

    # (in the functionalization metadata phase) Capture tokens after and see if
    # there are any differences (there are new effects or the token value for an
    # effect type has changed)
    tokens_after = dict(ctx.mode._tokens)
    discovered_effects = set()
    for effect_type, token in tokens_after.items():
        if effect_type not in tokens_before or tokens_before[effect_type] is not token:
            discovered_effects.add(effect_type)

    if discovered_effects:
        if not ctx.mode._allow_token_discovery:
            raise AssertionError(
                f"Number of tokens changed by {len(discovered_effects)} when tracing subgraph {subgraph}."
            )
        # Store discovered effects in the cache by identifier
        if invoke_subgraph_cache:
            invoke_subgraph_cache.add_effects(identifier, discovered_effects)

    return ctx.wrap_tensors(out)


def _(subgraph, identifier, *operands):
    from torch._dynamo.utils import dynamo_timed

    with dynamo_timed("invoke_subgraph_fake_tensor", log_pt2_compile_event=True):
        if getattr(subgraph, "_boxed_call", False):
            return subgraph(list(operands))
        return subgraph(*operands)


def _(proxy_mode: ProxyTorchDispatchMode, subgraph, identifier, *operands):
    # Check if we have already traced the subgraph.
    graph = None
    invoke_subgraph_cache = get_invoke_subgraph_cache()
    if invoke_subgraph_cache:
        graph = invoke_subgraph_cache.get_proxy_dispatch_entry(identifier)

    if graph is None:
        from torch._dynamo.utils import dynamo_timed

        with dynamo_timed("invoke_subgraph_proxy_tensor", log_pt2_compile_event=True):
            subgraph_decomp_table = _extract_nested_region_config(subgraph)

            # NB: invoke_subgraph subgraph re-trace seq_nr
            # The joint graph seq_nr will get wrong in the subsequent re-trace (all nodes will have the same seq_nr),
            # so we preserve the original graph's seq_nr here.
            with torch.fx.traceback._preserve_node_seq_nr():
                graph = reenter_make_fx(
                    subgraph, subgraph_decomp_table=subgraph_decomp_table
                )(*operands)

        from torch._guards import detect_fake_mode

        fake_mode = detect_fake_mode(operands)
        # Only insert deferred runtime asserts when we have dynamic shapes.
        # When shape_env is None (static shapes), there are no deferred asserts to insert.
        if fake_mode is not None and fake_mode.shape_env is not None:
            insert_deferred_runtime_asserts(
                graph,
                fake_mode.shape_env,
                "invoke_subgraph_proxy_torch_dispatch_mode",
                export=True,
            )
            graph.recompile()

        if not isinstance(proxy_mode.tracer, torch.fx.Tracer):
            raise AssertionError(
                f"expected proxy_mode.tracer to be torch.fx.Tracer, got {type(proxy_mode.tracer)}"
            )
        if invoke_subgraph_cache:
            invoke_subgraph_cache.add_proxy_dispatch_entry(identifier, graph)

    node_args = (graph, identifier, *operands)

    def _unwrap_proxy(arg):
        if isinstance(arg, torch.fx.GraphModule):
            # NOTE: [invoke_subgraph proxy_mode x auto_functionalize]
            # Previously, we assumed that `invoke_subgraph` would always be traced with the same tracer.
            # This allowed us to cache modules by their identifiers, assuming they were already registered.
            #
            # However, this assumption no longer holds when we auto-functionalize `invoke_subgraph`.
            # auto_functionalize functionalizes the subgraph and wrap it with `FunctionWithNoFreeVars`.
            # In the proxy mode implementation of `auto_functionalized_v2`, we need to materialize `FunctionWithNoFreeVars`
            # input as a graph module. To do this, we re-trace the `invoke_subgraph` hop, which starts a new sub-tracer
            # (see NOTE [materialize callable inputs as graph]). # When the new sub-tracer traces the `invoke_subgraph`
            # with a previously cached identifier, the corresponding graph module might not
            # exist as a submodule in the new tracer's root. Therefore, we register it as a submodule below.
            #
            # The alternative is to give a new identifier when we re-trace the invoke_subgraph but this will increase
            # the compilation time, which defeats the purpose of caching.
            registered_before = False
            for (
                _,
                submod,
            ) in proxy_mode.tracer.root.named_modules():  # type: ignore[union-attr]
                if arg is submod:
                    registered_before = True

            if not registered_before:
                qualname = proxy_mode.tracer.get_fresh_qualname("repeated_subgraph")  # type: ignore[union-attr]
                proxy_mode.tracer.root.register_module(qualname, arg)  # type: ignore[union-attr]
        return proxy_mode.tracer.unwrap_proxy(arg)  # type: ignore[union-attr]

    proxy_args = pytree.tree_map(_unwrap_proxy, node_args)  # type: ignore[union-attr]
    out_proxy = proxy_mode.tracer.create_proxy(
        "call_function", invoke_subgraph, proxy_args, {}
    )

    example_out = invoke_subgraph(graph, identifier, *operands)
    return track_tensor_tree(
        example_out, out_proxy, constant=None, tracer=proxy_mode.tracer
    )


def _(
    *,
    kernel_idx: int,
    constant_args_idx: int,
    grid: list["TritonGridType"],
    tma_descriptor_metadata: TMADescriptorMetadata,
    kwargs: dict[str, Any],
) -> None:
    return None


def _(additional_deps, subgraph, *args, **kwargs):
    """Fake tensor implementation - execute the subgraph."""
    return subgraph(*args, **kwargs)


def _(tensor: torch.Tensor) -> torch.Tensor:
    return torch.empty_like(tensor, device="cpu")


def _(
    tensor: torch.Tensor,
    device: torch.device,
) -> torch.Tensor:
    return torch.empty_like(tensor, device=device)


def _(*args: Any, **kwargs: Any) -> bool:
    # In namespace 'torch', the dictionary is always traversed in insertion order.
    # This function returns True.
    raise ValueError(
        "Should not be called directly "
        "because the original function will be called in the constant fold path."
    )


def _(
    from_index: int,  # kept to make stream transitions clearer
    to_index: int,
) -> None:
    pass


def _(
    from_index: int,
    to_index: int,
) -> None:
    pass


def _(
    event_index: int,
    stream_index: int,
) -> None:
    pass


def _(
    event_index: int,
    stream_index: int,
) -> None:
    pass


def _(event_index: int) -> None:
    pass


def _(device_type: str, device_index: int) -> None:
    pass


def _(stream_index: int) -> None:
    pass


def _(
    event_index: int,
    stream_index: int,
) -> None:
    pass


def _(
    wait_event_index: int,
    src_stream_index: int,
    to_dealloc: torch.Tensor,
) -> None:
    pass


def _(
    tensor: torch.Tensor,
    stream_index: int,
) -> None:
    pass


def _(x):
    return x.clone(), x.clone()


def _(x, y):
    if x.device != y.device:
        raise AssertionError(f"x.device={x.device} != y.device={y.device}")
    return (x * y).contiguous()


def _(x, *, scalar):
    return (x * scalar).contiguous()


def _(x, dim):
    return torch.empty_like(x), torch.empty_like(x, dtype=torch.long), torch.empty_like(x, dtype=torch.long)


def _(x, ind, ind_inv, dim):
    if x.device != ind.device:
        raise AssertionError(f"x.device={x.device} != ind.device={ind.device}")
    if x.device != ind_inv.device:
        raise AssertionError(f"x.device={x.device} != ind_inv.device={ind_inv.device}")
    if ind.dtype != torch.long:
        raise AssertionError(f"ind.dtype must be torch.long, got {ind.dtype}")
    if ind_inv.dtype != torch.long:
        raise AssertionError(f"ind_inv.dtype must be torch.long, got {ind_inv.dtype}")
    return torch.empty_like(x)


def _(x):
    ctx = torch._custom_op.impl.get_ctx()
    i0 = ctx.create_unbacked_symint()
    shape = [i0, x.dim()]
    result = x.new_empty(shape, dtype=torch.long)
    return result


def _(x, shape) -> Tensor:
    return x.clone().view(shape).clone()


def _(xs, dim):
    if len(xs) == 0:
        raise AssertionError("xs must not be empty")
    if not all(x.device == xs[0].device for x in xs):
        raise AssertionError("All tensors must be on the same device")
    if not all(x.dtype == xs[0].dtype for x in xs):
        raise AssertionError("All tensors must have the same dtype")
    return torch.cat(xs, dim=dim)


def _(x, splits, dim):
    return [xi.clone() for xi in torch.tensor_split(x, splits, dim)]


def _(x, splits, dim):
    return [xi.clone() for xi in torch.tensor_split(x, splits, dim)], len(splits)


def _(boxes, scores, iou_threshold):
    if boxes.device != scores.device:
        raise AssertionError(f"boxes.device={boxes.device} != scores.device={scores.device}")
    N = boxes.shape[0]
    if boxes.shape != (N, 4):
        raise AssertionError(f"boxes.shape must be (N, 4), got {boxes.shape}")
    if scores.shape != (N,):
        raise AssertionError(f"scores.shape must be (N,), got {scores.shape}")

    ctx = torch._custom_op.impl.get_ctx()
    i0 = ctx.create_unbacked_symint()
    result = boxes.new_empty([i0], dtype=torch.int64)
    return result


def _(x):
    return x.clone()


def _(x):
    return x.clone()


def _(x):
    return x.clone()


def _(
    inputs: Sequence[torch.Tensor],
    op_type: str,
    onnx_dtype: int,
    *,
    shape: Sequence[int | torch.SymInt],
    attr_keys: Sequence[str],
    attr_types: Sequence[str],
    attr_pos: Sequence[tuple[int, int]],
    attr_ints: Sequence[int],
    attr_floats: Sequence[float],
    attr_strs: Sequence[str],
    metadata_props_keys: Sequence[str] = (),
    metadata_props_values: Sequence[str] = (),
    domain: str = "",
    version: int | None = None,
) -> torch.Tensor:
    torch._check(
        onnx_dtype in _dtype_mappings.ONNX_DTYPE_TO_TORCH_DTYPE,
        lambda: f"{onnx_dtype} is invalid as an ONNX data type. Valid values are {list(_dtype_mappings.ONNX_DTYPE_TO_TORCH_DTYPE.keys())}",
    )
    # NOTE(justinchuby): Use zeros instead of torch.empty because I haven't figured
    # out how it can handle empty shapes
    return torch.zeros(
        shape, dtype=_dtype_mappings.ONNX_DTYPE_TO_TORCH_DTYPE[onnx_dtype]
    )


def _(
    inputs: Sequence[torch.Tensor],
    op_type: str,
    onnx_dtypes: Sequence[int],
    *,
    shapes: Sequence[Sequence[int | torch.SymInt]],
    attr_keys: Sequence[str],
    attr_types: Sequence[str],
    attr_pos: Sequence[tuple[int, int]],
    attr_ints: Sequence[int],
    attr_floats: Sequence[float],
    attr_strs: Sequence[str],
    metadata_props_keys: Sequence[str] = (),
    metadata_props_values: Sequence[str] = (),
    domain: str = "",
    version: int | None = None,
) -> list[torch.Tensor]:
    outputs = []
    torch._check(
        len(shapes) == len(onnx_dtypes),
        lambda: f"Number of shapes ({len(shapes)}) must match number of ONNX dtypes ({len(onnx_dtypes)})",
    )
    for shape, onnx_dtype in zip(shapes, onnx_dtypes):
        torch._check(
            onnx_dtype in _dtype_mappings.ONNX_DTYPE_TO_TORCH_DTYPE,
            lambda: f"{onnx_dtype} is invalid as an ONNX data type. Valid values are {list(_dtype_mappings.ONNX_DTYPE_TO_TORCH_DTYPE.keys())}",
        )
        # NOTE(justinchuby): Use zeros instead of torch.empty because I haven't figured
        # out how it can handle empty shapes
        outputs.append(
            torch.zeros(
                shape, dtype=_dtype_mappings.ONNX_DTYPE_TO_TORCH_DTYPE[onnx_dtype]
            )
        )
    return outputs


def _(
    k: torch.Tensor, v: torch.Tensor, seq_dim: int, pg_name: c10d.GroupName
) -> tuple[torch.Tensor, torch.Tensor]:
    shape_k = list(k.shape)
    shape_v = list(v.shape)
    shape_k[seq_dim] *= c10d._get_group_size_by_name(pg_name)
    shape_v[seq_dim] *= c10d._get_group_size_by_name(pg_name)
    new_k = torch.empty(shape_k, dtype=k.dtype, device=k.device)
    new_v = torch.empty(shape_v, dtype=v.dtype, device=v.device)
    return new_k, new_v


def _(
    grad_full_k: torch.Tensor,
    grad_full_v: torch.Tensor,
    seq_dim: int,
    pg_name: c10d.GroupName,
) -> tuple[torch.Tensor, torch.Tensor]:
    shape_k = list(grad_full_k.shape)
    shape_v = list(grad_full_v.shape)
    shape_k[seq_dim] //= c10d._get_group_size_by_name(pg_name)
    shape_v[seq_dim] //= c10d._get_group_size_by_name(pg_name)
    new_grad_k = torch.empty(
        shape_k, dtype=grad_full_k.dtype, device=grad_full_k.device
    )
    new_grad_v = torch.empty(
        shape_v, dtype=grad_full_v.dtype, device=grad_full_v.device
    )
    return new_grad_k, new_grad_v


def _(expr):
    arg = expr.args[0]
    return [Q.nonnegative(expr),
            Equivalent(~Q.zero(arg), ~Q.zero(expr)),
            Q.even(arg) >> Q.even(expr),
            Q.odd(arg) >> Q.odd(expr),
            Q.integer(arg) >> Q.integer(expr),
            ]


def _(expr):
    return [allargs(x, Q.positive(x), expr) >> Q.positive(expr),
            allargs(x, Q.negative(x), expr) >> Q.negative(expr),
            allargs(x, Q.real(x), expr) >> Q.real(expr),
            allargs(x, Q.rational(x), expr) >> Q.rational(expr),
            allargs(x, Q.integer(x), expr) >> Q.integer(expr),
            exactlyonearg(x, ~Q.integer(x), expr) >> ~Q.integer(expr),
            ]


def _(expr):
    allargs_real = allargs(x, Q.real(x), expr)
    onearg_irrational = exactlyonearg(x, Q.irrational(x), expr)
    return Implies(allargs_real, Implies(onearg_irrational, Q.irrational(expr)))


def _(expr):
    return [Equivalent(Q.zero(expr), anyarg(x, Q.zero(x), expr)),
            allargs(x, Q.positive(x), expr) >> Q.positive(expr),
            allargs(x, Q.real(x), expr) >> Q.real(expr),
            allargs(x, Q.rational(x), expr) >> Q.rational(expr),
            allargs(x, Q.integer(x), expr) >> Q.integer(expr),
            exactlyonearg(x, ~Q.rational(x), expr) >> ~Q.integer(expr),
            allargs(x, Q.commutative(x), expr) >> Q.commutative(expr),
            ]


def _(expr):
    # Implicitly assumes Mul has more than one arg
    # Would be allargs(x, Q.prime(x) | Q.composite(x)) except 1 is composite
    # More advanced prime assumptions will require inequalities, as 1 provides
    # a corner case.
    allargs_prime = allargs(x, Q.prime(x), expr)
    return Implies(allargs_prime, ~Q.prime(expr))


def _(expr):
    # General Case: Odd number of imaginary args implies mul is imaginary(To be implemented)
    allargs_imag_or_real = allargs(x, Q.imaginary(x) | Q.real(x), expr)
    onearg_imaginary = exactlyonearg(x, Q.imaginary(x), expr)
    return Implies(allargs_imag_or_real, Implies(onearg_imaginary, Q.imaginary(expr)))


def _(expr):
    allargs_real = allargs(x, Q.real(x), expr)
    onearg_irrational = exactlyonearg(x, Q.irrational(x), expr)
    return Implies(allargs_real, Implies(onearg_irrational, Q.irrational(expr)))


def _(expr):
    # Including the integer qualification means we don't need to add any facts
    # for odd, since the assumptions already know that every integer is
    # exactly one of even or odd.
    allargs_integer = allargs(x, Q.integer(x), expr)
    anyarg_even = anyarg(x, Q.even(x), expr)
    return Implies(allargs_integer, Equivalent(anyarg_even, Q.even(expr)))


def _(expr):
    allargs_square = allargs(x, Q.square(x), expr)
    allargs_invertible = allargs(x, Q.invertible(x), expr)
    return Implies(allargs_square, Equivalent(Q.invertible(expr), allargs_invertible))


def _(expr):
    base, exp = expr.base, expr.exp
    return [
        (Q.real(base) & Q.even(exp) & Q.nonnegative(exp)) >> Q.nonnegative(expr),
        (Q.nonnegative(base) & Q.odd(exp) & Q.nonnegative(exp)) >> Q.nonnegative(expr),
        (Q.nonpositive(base) & Q.odd(exp) & Q.nonnegative(exp)) >> Q.nonpositive(expr),
        Equivalent(Q.zero(expr), Q.zero(base) & Q.positive(exp))
    ]


def _(expr):
    ret = []
    for p, getter in _old_assump_getters.items():
        pred = p(expr)
        prop = getter(expr)
        if prop is not None:
            ret.append(Equivalent(pred, prop))
    return ret


def _(expr):
    return shape(expr.function)


def _(x):
    return any(is_random(i) for i in x)


def _(x):
    return True


def _(x):
    atoms = x.free_symbols
    return any(is_random(i) for i in atoms)


def _(x):
    return is_random(x.base)


def _(x):
    return True


def _(x):
    atoms = x.free_symbols
    if len(atoms) == 1 and next(iter(atoms)) == x:
        return False
    return any(is_random(i) for i in atoms)


def _(x):
    return True


def _(obj):
    return [ParametricRegion(obj.args)]


def _(obj):
    definition = obj.arbitrary_point(obj.parameter).args
    bounds = obj.limits
    return [ParametricRegion(definition, bounds)]


def _(obj, parameter='t'):
    definition = obj.arbitrary_point(parameter).args
    t = _symbol(parameter, real=True)
    bounds = (t, 0, 2*pi)
    return [ParametricRegion(definition, bounds)]


def _(obj, parameter='t'):
    t = _symbol(parameter, real=True)
    definition = obj.arbitrary_point(t).args

    for i in range(0, 3):
        lower_bound = solve(definition[i] - obj.points[0].args[i], t)
        upper_bound = solve(definition[i] - obj.points[1].args[i], t)

        if len(lower_bound) == 1 and len(upper_bound) == 1:
            bounds = t, lower_bound[0], upper_bound[0]
            break

    definition_tuple = obj.arbitrary_point(parameter).args
    return [ParametricRegion(definition_tuple, bounds)]


def _(obj, parameter='t'):
    l = [parametric_region_list(side, parameter)[0] for side in obj.sides]
    return l


def _(obj, parameters=('t', 's')):
    definition = obj.rational_parametrization(parameters)
    bounds = []

    for i in range(len(obj.variables) - 1):
        # Each parameter is replaced by its tangent to simplify integration
        parameter = _symbol(parameters[i], real=True)
        definition = [trigsimp(elem.subs(parameter, tan(parameter/2))) for elem in definition]
        bounds.append((parameter, 0, 2*pi),)

    definition = Tuple(*definition)
    return [ParametricRegion(definition, *bounds)]


def _(expr: Expr, x: _ArrayExpr):
    return ZeroArray(*x.shape)


def _(expr: ArrayTensorProduct, x: Expr):
    args = expr.args
    addend_list = []
    for i, arg in enumerate(expr.args):
        darg = array_derive(arg, x)
        if darg == 0:
            continue
        args_prev = args[:i]
        args_succ = args[i+1:]
        shape_prev = reduce(operator.add, map(get_shape, args_prev), ())
        shape_succ = reduce(operator.add, map(get_shape, args_succ), ())
        addend = _array_tensor_product(*args_prev, darg, *args_succ)
        tot1 = len(get_shape(x))
        tot2 = tot1 + len(shape_prev)
        tot3 = tot2 + len(get_shape(arg))
        tot4 = tot3 + len(shape_succ)
        perm = list(range(tot1, tot2)) + \
               list(range(tot1)) + list(range(tot2, tot3)) + \
               list(range(tot3, tot4))
        addend = _permute_dims(addend, _af_invert(perm))
        addend_list.append(addend)
    if len(addend_list) == 1:
        return addend_list[0]
    elif len(addend_list) == 0:
        return S.Zero
    else:
        return _array_add(*addend_list)


def _(expr: ArraySymbol, x: _ArrayExpr):
    if expr == x:
        return _permute_dims(
            ArrayTensorProduct.fromiter(Identity(i) for i in expr.shape),
            [2*i for i in range(len(expr.shape))] + [2*i+1 for i in range(len(expr.shape))]
        )
    return ZeroArray(*(x.shape + expr.shape))


def _(expr: MatrixSymbol, x: _ArrayExpr):
    m, n = expr.shape
    if expr == x:
        return _permute_dims(
            _array_tensor_product(Identity(m), Identity(n)),
            [0, 2, 1, 3]
        )
    return ZeroArray(*(x.shape + expr.shape))


def _(expr: Identity, x: _ArrayExpr):
    return ZeroArray(*(x.shape + expr.shape))


def _(expr: OneMatrix, x: _ArrayExpr):
    return ZeroArray(*(x.shape + expr.shape))


def _(expr: Transpose, x: Expr):
    # D(A.T, A) ==> (m,n,i,j) ==> D(A_ji, A_mn) = d_mj d_ni
    # D(B.T, A) ==> (m,n,i,j) ==> D(B_ji, A_mn)
    fd = array_derive(expr.arg, x)
    return _permute_dims(fd, [0, 1, 3, 2])


def _(expr: Inverse, x: Expr):
    mat = expr.I
    dexpr = array_derive(mat, x)
    tp = _array_tensor_product(-expr, dexpr, expr)
    mp = _array_contraction(tp, (1, 4), (5, 6))
    pp = _permute_dims(mp, [1, 2, 0, 3])
    return pp


def _(expr: ElementwiseApplyFunction, x: Expr):
    assert get_rank(expr) == 2
    assert get_rank(x) == 2
    fdiff = expr._get_function_fdiff()
    dexpr = array_derive(expr.expr, x)
    tp = _array_tensor_product(
        ElementwiseApplyFunction(fdiff, expr.expr),
        dexpr
    )
    td = _array_diagonal(
        tp, (0, 4), (1, 5)
    )
    return td


def _(expr: ArrayElementwiseApplyFunc, x: Expr):
    fdiff = expr._get_function_fdiff()
    subexpr = expr.expr
    dsubexpr = array_derive(subexpr, x)
    tp = _array_tensor_product(
        dsubexpr,
        ArrayElementwiseApplyFunc(fdiff, subexpr)
    )
    b = get_rank(x)
    c = get_rank(expr)
    diag_indices = [(b + i, b + c + i) for i in range(c)]
    return _array_diagonal(tp, *diag_indices)


def _(expr: MatrixExpr, x: Expr):
    cg = convert_matrix_to_array(expr)
    return array_derive(cg, x)


def _(expr: HadamardProduct, x: Expr):
    raise NotImplementedError()


def _(expr: ArrayContraction, x: Expr):
    fd = array_derive(expr.expr, x)
    rank_x = len(get_shape(x))
    contraction_indices = expr.contraction_indices
    new_contraction_indices = [tuple(j + rank_x for j in i) for i in contraction_indices]
    return _array_contraction(fd, *new_contraction_indices)


def _(expr: ArrayDiagonal, x: Expr):
    dsubexpr = array_derive(expr.expr, x)
    rank_x = len(get_shape(x))
    diag_indices = [[j + rank_x for j in i] for i in expr.diagonal_indices]
    return _array_diagonal(dsubexpr, *diag_indices)


def _(expr: ArrayAdd, x: Expr):
    return _array_add(*[array_derive(arg, x) for arg in expr.args])


def _(expr: PermuteDims, x: Expr):
    de = array_derive(expr.expr, x)
    perm = [0, 1] + [i + 2 for i in expr.permutation.array_form]
    return _permute_dims(de, perm)


def _(expr: Reshape, x: Expr):
    de = array_derive(expr.expr, x)
    return Reshape(de, get_shape(x) + expr.shape)


def _(expr: ZeroArray):
    if get_rank(expr) == 2:
        return ZeroMatrix(*expr.shape)
    else:
        return expr


def _(expr: ArrayTensorProduct):
    return _a2m_tensor_product(*[_array2matrix(arg) for arg in expr.args])


def _(expr: ArrayContraction):
    expr = expr.flatten_contraction_of_diagonal()
    expr = identify_removable_identity_matrices(expr)
    expr = expr.split_multiple_contractions()
    expr = identify_hadamard_products(expr)
    if not isinstance(expr, ArrayContraction):
        return _array2matrix(expr)
    subexpr = expr.expr
    contraction_indices: tuple[tuple[int]] = expr.contraction_indices
    if contraction_indices == ((0,), (1,)) or (
        contraction_indices == ((0,),) and subexpr.shape[1] == 1
    ) or (
        contraction_indices == ((1,),) and subexpr.shape[0] == 1
    ):
        shape = subexpr.shape
        subexpr = _array2matrix(subexpr)
        if isinstance(subexpr, MatrixExpr):
            return OneMatrix(1, shape[0])*subexpr*OneMatrix(shape[1], 1)
    if isinstance(subexpr, ArrayTensorProduct):
        newexpr = _array_contraction(_array2matrix(subexpr), *contraction_indices)
        contraction_indices = newexpr.contraction_indices
        if any(i > 2 for i in newexpr.subranks):
            addends = _array_add(*[_a2m_tensor_product(*j) for j in itertools.product(*[i.args if isinstance(i,
                                                                                                                             ArrayAdd) else [i] for i in expr.expr.args])])
            newexpr = _array_contraction(addends, *contraction_indices)
        if isinstance(newexpr, ArrayAdd):
            ret = _array2matrix(newexpr)
            return ret
        assert isinstance(newexpr, ArrayContraction)
        ret = _support_function_tp1_recognize(contraction_indices, list(newexpr.expr.args))
        return ret
    elif not isinstance(subexpr, _CodegenArrayAbstract):
        ret = _array2matrix(subexpr)
        if isinstance(ret, MatrixExpr):
            assert expr.contraction_indices == ((0, 1),)
            return _a2m_trace(ret)
        else:
            return _array_contraction(ret, *expr.contraction_indices)


def _(expr: ArrayDiagonal):
    pexpr = _array_diagonal(_array2matrix(expr.expr), *expr.diagonal_indices)
    pexpr = identify_hadamard_products(pexpr)
    if isinstance(pexpr, ArrayDiagonal):
        pexpr = _array_diag2contr_diagmatrix(pexpr)
    if expr == pexpr:
        return expr
    return _array2matrix(pexpr)


def _(expr: PermuteDims):
    if expr.permutation.array_form == [1, 0]:
        return _a2m_transpose(_array2matrix(expr.expr))
    elif isinstance(expr.expr, ArrayTensorProduct):
        ranks = expr.expr.subranks
        inv_permutation = expr.permutation**(-1)
        newrange = [inv_permutation(i) for i in range(sum(ranks))]
        newpos = []
        counter = 0
        for rank in ranks:
            newpos.append(newrange[counter:counter+rank])
            counter += rank
        newargs = []
        newperm = []
        scalars = []
        for pos, arg in zip(newpos, expr.expr.args):
            if len(pos) == 0:
                scalars.append(_array2matrix(arg))
            elif pos == sorted(pos):
                newargs.append((_array2matrix(arg), pos[0]))
                newperm.extend(pos)
            elif len(pos) == 2:
                newargs.append((_a2m_transpose(_array2matrix(arg)), pos[0]))
                newperm.extend(reversed(pos))
            else:
                raise NotImplementedError()
        newargs = [i[0] for i in newargs]
        return _permute_dims(_a2m_tensor_product(*scalars, *newargs), _af_invert(newperm))
    elif isinstance(expr.expr, ArrayContraction):
        mat_mul_lines = _array2matrix(expr.expr)
        if not isinstance(mat_mul_lines, ArrayTensorProduct):
            return _permute_dims(mat_mul_lines, expr.permutation)
        # TODO: this assumes that all arguments are matrices, it may not be the case:
        permutation = Permutation(2*len(mat_mul_lines.args)-1)*expr.permutation
        permuted = [permutation(i) for i in range(2*len(mat_mul_lines.args))]
        args_array = [None for i in mat_mul_lines.args]
        for i in range(len(mat_mul_lines.args)):
            p1 = permuted[2*i]
            p2 = permuted[2*i+1]
            if p1 // 2 != p2 // 2:
                return _permute_dims(mat_mul_lines, permutation)
            if p1 > p2:
                args_array[i] = _a2m_transpose(mat_mul_lines.args[p1 // 2])
            else:
                args_array[i] = mat_mul_lines.args[p1 // 2]
        return _a2m_tensor_product(*args_array)
    else:
        return expr


def _(expr: ArrayAdd):
    addends = [_array2matrix(arg) for arg in expr.args]
    return _a2m_add(*addends)


def _(expr: ArrayElementwiseApplyFunc):
    subexpr = _array2matrix(expr.expr)
    if isinstance(subexpr, MatrixExpr):
        if subexpr.shape != (1, 1):
            d = expr.function.bound_symbols[0]
            w = Wild("w", exclude=[d])
            p = Wild("p", exclude=[d])
            m = expr.function.expr.match(w*d**p)
            if m is not None:
                return m[w]*HadamardPower(subexpr, m[p])
        return ElementwiseApplyFunction(expr.function, subexpr)
    else:
        return ArrayElementwiseApplyFunc(expr.function, subexpr)


def _(expr: ArrayElement):
    ret = _array2matrix(expr.name)
    if isinstance(ret, MatrixExpr):
        return MatrixElement(ret, *expr.indices)
    return ArrayElement(ret, expr.indices)


def _(expr: ArrayTensorProduct):
    # Recognize expressions like [x, y] with shape (k, 1, k, 1) as `x*y.T`.
    # The matrix expression has to be equivalent to the tensor product of the
    # matrices, with trivial dimensions (i.e. dim=1) dropped.
    # That is, add contractions over trivial dimensions:

    removed = []
    newargs = []
    cumul = list(accumulate([0] + [get_rank(arg) for arg in expr.args]))
    pending = None
    prev_i = None
    for i, arg in enumerate(expr.args):
        current_range = list(range(cumul[i], cumul[i+1]))
        if isinstance(arg, OneArray):
            removed.extend(current_range)
            continue
        if not isinstance(arg, (MatrixExpr, MatrixBase)):
            rarg, rem = _remove_trivial_dims(arg)
            removed.extend(rem)
            newargs.append(rarg)
            continue
        elif getattr(arg, "is_Identity", False) and arg.shape == (1, 1):
            if arg.shape == (1, 1):
                # Ignore identity matrices of shape (1, 1) - they are equivalent to scalar 1.
                removed.extend(current_range)
            continue
        elif arg.shape == (1, 1):
            arg, _ = _remove_trivial_dims(arg)
            # Matrix is equivalent to scalar:
            if len(newargs) == 0:
                newargs.append(arg)
            elif 1 in get_shape(newargs[-1]):
                if newargs[-1].shape[1] == 1:
                    newargs[-1] = newargs[-1]*arg
                else:
                    newargs[-1] = arg*newargs[-1]
                removed.extend(current_range)
            else:
                newargs.append(arg)
        elif 1 in arg.shape:
            k = [i for i in arg.shape if i != 1][0]
            if pending is None:
                pending = k
                prev_i = i
                newargs.append(arg)
            elif pending == k:
                prev = newargs[-1]
                if prev.shape[0] == 1:
                    d1 = cumul[prev_i]  # type: ignore
                    prev = _a2m_transpose(prev)
                else:
                    d1 = cumul[prev_i] + 1  # type: ignore
                if arg.shape[1] == 1:
                    d2 = cumul[i] + 1
                    arg = _a2m_transpose(arg)
                else:
                    d2 = cumul[i]
                newargs[-1] = prev*arg
                pending = None
                removed.extend([d1, d2])
            else:
                newargs.append(arg)
                pending = k
                prev_i = i
        else:
            newargs.append(arg)
            pending = None
    newexpr, newremoved = _a2m_tensor_product(*newargs), sorted(removed)
    if isinstance(newexpr, ArrayTensorProduct):
        newexpr, newremoved2 = _find_trivial_matrices_rewrite(newexpr)
        newremoved = _combine_removed(-1, newremoved, newremoved2)
    if isinstance(newexpr, ArrayTensorProduct):
        newexpr, newremoved2 = _find_trivial_kronecker_products_broadcast(newexpr)
        newremoved = _combine_removed(-1, newremoved, newremoved2)
    return newexpr, newremoved


def _(expr: ArrayAdd):
    rec = [_remove_trivial_dims(arg) for arg in expr.args]
    newargs, removed = zip(*rec)
    if len({get_shape(i) for i in newargs}) > 1:
        return expr, []
    if len(removed) == 0:
        return expr, removed
    removed1 = removed[0]
    return _a2m_add(*newargs), removed1


def _(expr: PermuteDims):
    subexpr, subremoved = _remove_trivial_dims(expr.expr)
    p = expr.permutation.array_form
    pinv = _af_invert(expr.permutation.array_form)
    shift = list(accumulate([1 if i in subremoved else 0 for i in range(len(p))]))
    premoved = [pinv[i] for i in subremoved]
    p2 = [e - shift[e] for e in p if e not in subremoved]
    # TODO: check if subremoved should be permuted as well...
    newexpr = _permute_dims(subexpr, p2)
    premoved = sorted(premoved)
    if newexpr != expr:
        newexpr, removed2 = _remove_trivial_dims(_array2matrix(newexpr))
        premoved = _combine_removed(-1, premoved, removed2)
    return newexpr, premoved


def _(expr: ArrayContraction):
    new_expr, removed0 = _array_contraction_to_diagonal_multiple_identity(expr)
    if new_expr != expr:
        new_expr2, removed1 = _remove_trivial_dims(_array2matrix(new_expr))
        removed = _combine_removed(-1, removed0, removed1)
        return new_expr2, removed
    rank1 = get_rank(expr)
    expr, removed1 = remove_identity_matrices(expr)
    if not isinstance(expr, ArrayContraction):
        expr2, removed2 = _remove_trivial_dims(expr)
        return expr2, _combine_removed(rank1, removed1, removed2)
    newexpr, removed2 = _remove_trivial_dims(expr.expr)
    shifts = list(accumulate([1 if i in removed2 else 0 for i in range(get_rank(expr.expr))]))
    new_contraction_indices = [tuple(j for j in i if j not in removed2) for i in expr.contraction_indices]
    # Remove possible empty tuples "()":
    new_contraction_indices = [i for i in new_contraction_indices if len(i) > 0]
    contraction_indices_flat = [j for i in expr.contraction_indices for j in i]
    removed2 = [i for i in removed2 if i not in contraction_indices_flat]
    new_contraction_indices = [tuple(j - shifts[j] for j in i) for i in new_contraction_indices]
    # Shift removed2:
    removed2 = ArrayContraction._push_indices_up(expr.contraction_indices, removed2)
    removed = _combine_removed(rank1, removed1, removed2)
    return _array_contraction(newexpr, *new_contraction_indices), list(removed)


def _(expr: ArrayDiagonal):
    newexpr, removed = _remove_trivial_dims(expr.expr)
    shifts = list(accumulate([0] + [1 if i in removed else 0 for i in range(get_rank(expr.expr))]))
    new_diag_indices_map = {i: tuple(j for j in i if j not in removed) for i in expr.diagonal_indices}
    for old_diag_tuple, new_diag_tuple in new_diag_indices_map.items():
        if len(new_diag_tuple) == 1:
            removed = [i for i in removed if i not in old_diag_tuple]
    new_diag_indices = [tuple(j - shifts[j] for j in i) for i in new_diag_indices_map.values()]
    rank = get_rank(expr.expr)
    removed = ArrayDiagonal._push_indices_up(expr.diagonal_indices, removed, rank)
    removed = sorted(set(removed))
    # If there are single axes to diagonalize remaining, it means that their
    # corresponding dimension has been removed, they no longer need diagonalization:
    new_diag_indices = [i for i in new_diag_indices if len(i) > 0]
    if len(new_diag_indices) > 0:
        newexpr2 = _array_diagonal(newexpr, *new_diag_indices, allow_trivial_diags=True)
    else:
        newexpr2 = newexpr
    if isinstance(newexpr2, ArrayDiagonal):
        newexpr3, removed2 = _remove_diagonalized_identity_matrices(newexpr2)
        removed = _combine_removed(-1, removed, removed2)
        return newexpr3, removed
    else:
        return newexpr2, removed


def _(expr: ElementwiseApplyFunction):
    subexpr, removed = _remove_trivial_dims(expr.expr)
    if subexpr.shape == (1, 1):
        # TODO: move this to ElementwiseApplyFunction
        return expr.function(subexpr), removed + [0, 1]
    return ElementwiseApplyFunction(expr.function, subexpr), []


def _(expr: ArrayElementwiseApplyFunc):
    subexpr, removed = _remove_trivial_dims(expr.expr)
    return ArrayElementwiseApplyFunc(expr.function, subexpr), removed


def _(dist: BetaDistribution, size, rand_state):
    return rand_state.beta(a=float(dist.alpha), b=float(dist.beta), size=size)


def _(dist: ChiSquaredDistribution, size, rand_state):
    return rand_state.chisquare(df=float(dist.k), size=size)


def _(dist: ExponentialDistribution, size, rand_state):
    return rand_state.exponential(1 / float(dist.rate), size=size)


def _(dist: FDistributionDistribution, size, rand_state):
    return rand_state.f(dfnum = float(dist.d1), dfden = float(dist.d2), size=size)


def _(dist: GammaDistribution, size, rand_state):
    return rand_state.gamma(shape = float(dist.k), scale = float(dist.theta), size=size)


def _(dist: GumbelDistribution, size, rand_state):
    return rand_state.gumbel(loc = float(dist.mu), scale = float(dist.beta), size=size)


def _(dist: LaplaceDistribution, size, rand_state):
    return rand_state.laplace(loc = float(dist.mu), scale = float(dist.b), size=size)


def _(dist: LogisticDistribution, size, rand_state):
    return rand_state.logistic(loc = float(dist.mu), scale = float(dist.s), size=size)


def _(dist: LogNormalDistribution, size, rand_state):
    return rand_state.lognormal(mean = float(dist.mean), sigma = float(dist.std), size=size)


def _(dist: NormalDistribution, size, rand_state):
    return rand_state.normal(loc = float(dist.mean), scale = float(dist.std), size=size)


def _(dist: RayleighDistribution, size, rand_state):
    return rand_state.rayleigh(scale = float(dist.sigma), size=size)


def _(dist: ParetoDistribution, size, rand_state):
    return (numpy.random.pareto(a=float(dist.alpha), size=size) + 1) * float(dist.xm)


def _(dist: TriangularDistribution, size, rand_state):
    return rand_state.triangular(left = float(dist.a), mode = float(dist.b), right = float(dist.c), size=size)


def _(dist: UniformDistribution, size, rand_state):
    return rand_state.uniform(low=float(dist.left), high=float(dist.right), size=size)


def _(dist: GeometricDistribution, size, rand_state):
    return rand_state.geometric(p=float(dist.p), size=size)


def _(dist: PoissonDistribution, size, rand_state):
    return rand_state.poisson(lam=float(dist.lamda), size=size)


def _(dist: ZetaDistribution, size, rand_state):
    return rand_state.zipf(a=float(dist.s), size=size)


def _(dist: BinomialDistribution, size, rand_state):
    return rand_state.binomial(n=int(dist.n), p=float(dist.p), size=size)


def _(dist: HypergeometricDistribution, size, rand_state):
    return rand_state.hypergeometric(ngood = int(dist.N), nbad = int(dist.m), nsample = int(dist.n), size=size)


def _(dist: BetaDistribution):
    return pymc.Beta('X', alpha=float(dist.alpha), beta=float(dist.beta))


def _(dist: CauchyDistribution):
    return pymc.Cauchy('X', alpha=float(dist.x0), beta=float(dist.gamma))


def _(dist: ChiSquaredDistribution):
    return pymc.ChiSquared('X', nu=float(dist.k))


def _(dist: ExponentialDistribution):
    return pymc.Exponential('X', lam=float(dist.rate))


def _(dist: GammaDistribution):
    return pymc.Gamma('X', alpha=float(dist.k), beta=1 / float(dist.theta))


def _(dist: LogNormalDistribution):
    return pymc.Lognormal('X', mu=float(dist.mean), sigma=float(dist.std))


def _(dist: NormalDistribution):
    return pymc.Normal('X', float(dist.mean), float(dist.std))


def _(dist: GaussianInverseDistribution):
    return pymc.Wald('X', mu=float(dist.mean), lam=float(dist.shape))


def _(dist: ParetoDistribution):
    return pymc.Pareto('X', alpha=float(dist.alpha), m=float(dist.xm))


def _(dist: UniformDistribution):
    return pymc.Uniform('X', lower=float(dist.left), upper=float(dist.right))


def _(dist: GeometricDistribution):
    return pymc.Geometric('X', p=float(dist.p))


def _(dist: NegativeBinomialDistribution):
    return pymc.NegativeBinomial('X', mu=float((dist.p * dist.r) / (1 - dist.p)),
                                  alpha=float(dist.r))


def _(dist: PoissonDistribution):
    return pymc.Poisson('X', mu=float(dist.lamda))


def _(dist: BernoulliDistribution):
    return pymc.Bernoulli('X', p=float(dist.p))


def _(dist: BinomialDistribution):
    return pymc.Binomial('X', n=int(dist.n), p=float(dist.p))


def _(dist: SingleContinuousDistribution, size, seed):
    # if we don't need to make a handmade pdf, we won't
    import scipy.stats

    z = Dummy('z')
    handmade_pdf = lambdify(z, dist.pdf(z), ['numpy', 'scipy'])

    class scipy_pdf(scipy.stats.rv_continuous):
        def _pdf(dist, x):
            return handmade_pdf(x)

    scipy_rv = scipy_pdf(a=float(dist.set._inf),
                         b=float(dist.set._sup), name='scipy_pdf')
    return scipy_rv.rvs(size=size, random_state=seed)


def _(dist: ChiSquaredDistribution, size, seed):
    # same parametrisation
    return scipy.stats.chi2.rvs(df=float(dist.k), size=size, random_state=seed)


def _(dist: ExponentialDistribution, size, seed):
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.expon.html#scipy.stats.expon
    return scipy.stats.expon.rvs(scale=1 / float(dist.rate), size=size, random_state=seed)


def _(dist: GammaDistribution, size, seed):
    # https://stackoverflow.com/questions/42150965/how-to-plot-gamma-distribution-with-alpha-and-beta-parameters-in-python
    return scipy.stats.gamma.rvs(a=float(dist.k), scale=float(dist.theta), size=size, random_state=seed)


def _(dist: LogNormalDistribution, size, seed):
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.lognorm.html
    return scipy.stats.lognorm.rvs(scale=float(exp(dist.mean)), s=float(dist.std), size=size, random_state=seed)


def _(dist: NormalDistribution, size, seed):
    return scipy.stats.norm.rvs(loc=float(dist.mean), scale=float(dist.std), size=size, random_state=seed)


def _(dist: ParetoDistribution, size, seed):
    # https://stackoverflow.com/questions/42260519/defining-pareto-distribution-in-python-scipy
    return scipy.stats.pareto.rvs(b=float(dist.alpha), scale=float(dist.xm), size=size, random_state=seed)


def _(dist: StudentTDistribution, size, seed):
    return scipy.stats.t.rvs(df=float(dist.nu), size=size, random_state=seed)


def _(dist: UniformDistribution, size, seed):
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.uniform.html
    return scipy.stats.uniform.rvs(loc=float(dist.left), scale=float(dist.right - dist.left), size=size, random_state=seed)


def _(dist: BetaDistribution, size, seed):
    # same parametrisation
    return scipy.stats.beta.rvs(a=float(dist.alpha), b=float(dist.beta), size=size, random_state=seed)


def _(dist: CauchyDistribution, size, seed):
    return scipy.stats.cauchy.rvs(loc=float(dist.x0), scale=float(dist.gamma), size=size, random_state=seed)


def _(dist: DiscreteDistributionHandmade, size, seed):
    from scipy.stats import rv_discrete

    z = Dummy('z')
    handmade_pmf = lambdify(z, dist.pdf(z), ['numpy', 'scipy'])

    class scipy_pmf(rv_discrete):
        def _pmf(dist, x):
            return handmade_pmf(x)

    scipy_rv = scipy_pmf(a=float(dist.set._inf), b=float(dist.set._sup),
                         name='scipy_pmf')
    return scipy_rv.rvs(size=size, random_state=seed)


def _(dist: GeometricDistribution, size, seed):
    return scipy.stats.geom.rvs(p=float(dist.p), size=size, random_state=seed)


def _(dist: LogarithmicDistribution, size, seed):
    return scipy.stats.logser.rvs(p=float(dist.p), size=size, random_state=seed)


def _(dist: NegativeBinomialDistribution, size, seed):
    return scipy.stats.nbinom.rvs(n=float(dist.r), p=float(dist.p), size=size, random_state=seed)


def _(dist: PoissonDistribution, size, seed):
    return scipy.stats.poisson.rvs(mu=float(dist.lamda), size=size, random_state=seed)


def _(dist: SkellamDistribution, size, seed):
    return scipy.stats.skellam.rvs(mu1=float(dist.mu1), mu2=float(dist.mu2), size=size, random_state=seed)


def _(dist: YuleSimonDistribution, size, seed):
    return scipy.stats.yulesimon.rvs(alpha=float(dist.rho), size=size, random_state=seed)


def _(dist: ZetaDistribution, size, seed):
    return scipy.stats.zipf.rvs(a=float(dist.s), size=size, random_state=seed)


def _(dist: SingleFiniteDistribution, size, seed):
    # scipy can handle with custom distributions

    from scipy.stats import rv_discrete
    density_ = dist.dict
    x, y = [], []
    for k, v in density_.items():
        x.append(int(k))
        y.append(float(v))
    scipy_rv = rv_discrete(name='scipy_rv', values=(x, y))
    return scipy_rv.rvs(size=size, random_state=seed)


def _(x, y):
    return None


def _(x, y):
    return x+y


def _(x, y):
    """
    Additions in interval arithmetic
    https://en.wikipedia.org/wiki/Interval_arithmetic
    """
    return Interval(x.start + y.start, x.end + y.end,
                    x.left_open or y.left_open, x.right_open or y.right_open)


def _(x, y):
    if x.start is S.NegativeInfinity:
        return Interval(-oo, oo)
    return FiniteSet({S.Infinity})


def _(x, y):
    if x.end is S.Infinity:
        return Interval(-oo, oo)
    return FiniteSet({S.NegativeInfinity})


def _(x, y):
    return None


def _(x, y):
    return x-y


def _(x, y):
    """
    Subtractions in interval arithmetic
    https://en.wikipedia.org/wiki/Interval_arithmetic
    """
    return Interval(x.start - y.end, x.end - y.start,
                    x.left_open or y.right_open, x.right_open or y.left_open)


def _(x, y):
    if x.start is S.NegativeInfinity:
        return Interval(-oo, oo)
    return FiniteSet(-oo)


def _(x, y):
    if x.start is S.NegativeInfinity:
        return Interval(-oo, oo)
    return FiniteSet(-oo)


def _(f, x):
    return None


def _(f, x):
    return FiniteSet(*map(f, x))


def _(f, x):
    from sympy.solvers.solveset import solveset
    from sympy.series import limit
    # TODO: handle functions with infinitely many solutions (eg, sin, tan)
    # TODO: handle multivariate functions

    expr = f.expr
    if len(expr.free_symbols) > 1 or len(f.variables) != 1:
        return
    var = f.variables[0]
    if not var.is_real:
        if expr.subs(var, Dummy(real=True)).is_real is False:
            return

    if expr.is_Piecewise:
        result = S.EmptySet
        domain_set = x
        for (p_expr, p_cond) in expr.args:
            if p_cond is true:
                intrvl = domain_set
            else:
                intrvl = p_cond.as_set()
                intrvl = Intersection(domain_set, intrvl)

            if p_expr.is_Number:
                image = FiniteSet(p_expr)
            else:
                image = imageset(Lambda(var, p_expr), intrvl)
            result = Union(result, image)

            # remove the part which has been `imaged`
            domain_set = Complement(domain_set, intrvl)
            if domain_set is S.EmptySet:
                break
        return result

    if not x.start.is_comparable or not x.end.is_comparable:
        return

    try:
        from sympy.polys.polyutils import _nsort
        sing = list(singularities(expr, var, x))
        if len(sing) > 1:
            sing = _nsort(sing)
    except NotImplementedError:
        return

    if x.left_open:
        _start = limit(expr, var, x.start, dir="+")
    elif x.start not in sing:
        _start = f(x.start)
    if x.right_open:
        _end = limit(expr, var, x.end, dir="-")
    elif x.end not in sing:
        _end = f(x.end)

    if len(sing) == 0:
        soln_expr = solveset(diff(expr, var), var)
        if not (isinstance(soln_expr, FiniteSet)
                or soln_expr is S.EmptySet):
            return
        solns = list(soln_expr)

        extr = [_start, _end] + [f(i) for i in solns
                                 if i.is_real and i in x]
        start, end = Min(*extr), Max(*extr)

        left_open, right_open = False, False
        if _start <= _end:
            # the minimum or maximum value can occur simultaneously
            # on both the edge of the interval and in some interior
            # point
            if start == _start and start not in solns:
                left_open = x.left_open
            if end == _end and end not in solns:
                right_open = x.right_open
        else:
            if start == _end and start not in solns:
                left_open = x.right_open
            if end == _start and end not in solns:
                right_open = x.left_open

        return Interval(start, end, left_open, right_open)
    else:
        return imageset(f, Interval(x.start, sing[0],
                                    x.left_open, True)) + \
            Union(*[imageset(f, Interval(sing[i], sing[i + 1], True, True))
                    for i in range(0, len(sing) - 1)]) + \
            imageset(f, Interval(sing[-1], x.end, True, x.right_open))


def _(f, x):
    if f == exp:
        return Interval(exp(x.start), exp(x.end), x.left_open, x.right_open)
    elif f == log:
        return Interval(log(x.start), log(x.end), x.left_open, x.right_open)
    return ImageSet(Lambda(_x, f(_x)), x)


def _(f, x):
    return Union(*(imageset(f, arg) for arg in x.args))


def _(f, x):
    # If the function is invertible, intersect the maps of the sets.
    if is_function_invertible_in_set(f, x):
        return Intersection(*(imageset(f, arg) for arg in x.args))
    else:
        return ImageSet(Lambda(_x, f(_x)), x)


def _(f, x):
    return x


def _(f, x):
    return ImageSet(Lambda(_x, f(_x)), x)


def _(f, self):
    if not self:
        return S.EmptySet
    if not isinstance(f.expr, Expr):
        return
    if self.size == 1:
        return FiniteSet(f(self[0]))
    if f is S.IdentityFunction:
        return self

    x = f.variables[0]
    expr = f.expr
    # handle f that is linear in f's variable
    if x not in expr.free_symbols or x in expr.diff(x).free_symbols:
        return
    if self.start.is_finite:
        F = f(self.step*x + self.start)  # for i in range(len(self))
    else:
        F = f(-self.step*x + self[-1])
    F = expand_mul(F)
    if F != expr:
        return imageset(x, F, Range(self.size))


def _(f, self):
    expr = f.expr
    if not isinstance(expr, Expr):
        return

    n = f.variables[0]
    if expr == abs(n):
        return S.Naturals0

    # f(x) + c and f(-x) + c cover the same integers
    # so choose the form that has the fewest negatives
    c = f(0)
    fx = f(n) - c
    f_x = f(-n) - c
    neg_count = lambda e: sum(_.could_extract_minus_sign()
        for _ in Add.make_args(e))
    if neg_count(f_x) < neg_count(fx):
        expr = f_x + c

    a = Wild('a', exclude=[n])
    b = Wild('b', exclude=[n])
    match = expr.match(a*n + b)
    if match and match[a] and (
            not match[a].atoms(Float) and
            not match[b].atoms(Float)):
        # canonical shift
        a, b = match[a], match[b]
        if a in [1, -1]:
            # drop integer addends in b
            nonint = []
            for bi in Add.make_args(b):
                if not bi.is_integer:
                    nonint.append(bi)
            b = Add(*nonint)
        if b.is_number and a.is_real:
            # avoid Mod for complex numbers, #11391
            br, bi = match_real_imag(b)
            if br and br.is_comparable and a.is_comparable:
                br %= a
                b = br + S.ImaginaryUnit*bi
        elif b.is_number and a.is_imaginary:
            br, bi = match_real_imag(b)
            ai = a/S.ImaginaryUnit
            if bi and bi.is_comparable and ai.is_comparable:
                bi %= ai
                b = br + S.ImaginaryUnit*bi
        expr = a*n + b

    if expr != f.expr:
        return ImageSet(Lambda(n, expr), S.Integers)


def _(f, self):
    expr = f.expr
    if not isinstance(expr, Expr):
        return

    x = f.variables[0]
    if not expr.free_symbols - {x}:
        if expr == abs(x):
            if self is S.Naturals:
                return self
            return S.Naturals0
        step = expr.coeff(x)
        c = expr.subs(x, 0)
        if c.is_Integer and step.is_Integer and expr == step*x + c:
            if self is S.Naturals:
                c += step
            if step > 0:
                if step == 1:
                    if c == 0:
                        return S.Naturals0
                    elif c == 1:
                        return S.Naturals
                return Range(c, oo, step)
            return Range(c, -oo, step)


def _(f, self):
    expr = f.expr
    if not isinstance(expr, Expr):
        return
    return _set_function(f, Interval(-oo, oo))


def _(a, b):
    return None


def _(a, b):
    return ConditionSet(a.sym, a.condition, Intersection(a.base_set, b))


def _(a, b):
    return a


def _(a, b):
    return a if a is S.Naturals else b


def _(a, b):
    return intersection_sets(b, a)


def _(self, other):
    if other.is_ComplexRegion:
        # self in rectangular form
        if (not self.polar) and (not other.polar):
            return ComplexRegion(Intersection(self.sets, other.sets))

        # self in polar form
        elif self.polar and other.polar:
            r1, theta1 = self.a_interval, self.b_interval
            r2, theta2 = other.a_interval, other.b_interval
            new_r_interval = Intersection(r1, r2)
            new_theta_interval = Intersection(theta1, theta2)

            # 0 and 2*Pi means the same
            if ((2*S.Pi in theta1 and S.Zero in theta2) or
               (2*S.Pi in theta2 and S.Zero in theta1)):
                new_theta_interval = Union(new_theta_interval,
                                           FiniteSet(0))
            return ComplexRegion(new_r_interval*new_theta_interval,
                                polar=True)


    if other.is_subset(S.Reals):
        new_interval = []
        x = symbols("x", cls=Dummy, real=True)

        # self in rectangular form
        if not self.polar:
            for element in self.psets:
                if S.Zero in element.args[1]:
                    new_interval.append(element.args[0])
            new_interval = Union(*new_interval)
            return Intersection(new_interval, other)

        # self in polar form
        elif self.polar:
            for element in self.psets:
                if S.Zero in element.args[1]:
                    new_interval.append(element.args[0])
                if S.Pi in element.args[1]:
                    new_interval.append(ImageSet(Lambda(x, -x), element.args[0]))
                if S.Zero in element.args[0]:
                    new_interval.append(FiniteSet(0))
            new_interval = Union(*new_interval)
            return Intersection(new_interval, other)


def _(a, b):
    return a


def _(a, b):
    # Check that there are no symbolic arguments
    if not all(i.is_number for i in a.args + b.args[:2]):
        return

    # In case of null Range, return an EmptySet.
    if a.size == 0:
        return S.EmptySet

    # trim down to self's size, and represent
    # as a Range with step 1.
    start = ceiling(max(b.inf, a.inf))
    if start not in b:
        start += 1
    end = floor(min(b.sup, a.sup))
    if end not in b:
        end -= 1
    return intersection_sets(a, Range(start, end + 1))


def _(a, b):
    return intersection_sets(a, Interval(b.inf, S.Infinity))


def _(a, b):
    # Check that there are no symbolic range arguments
    if not all(all(v.is_number for v in r.args) for r in [a, b]):
        return None

    # non-overlap quick exits
    if not b:
        return S.EmptySet
    if not a:
        return S.EmptySet
    if b.sup < a.inf:
        return S.EmptySet
    if b.inf > a.sup:
        return S.EmptySet

    # work with finite end at the start
    r1 = a
    if r1.start.is_infinite:
        r1 = r1.reversed
    r2 = b
    if r2.start.is_infinite:
        r2 = r2.reversed

    # If both ends are infinite then it means that one Range is just the set
    # of all integers (the step must be 1).
    if r1.start.is_infinite:
        return b
    if r2.start.is_infinite:
        return a

    from sympy.solvers.diophantine.diophantine import diop_linear

    # this equation represents the values of the Range;
    # it's a linear equation
    eq = lambda r, i: r.start + i*r.step

    # we want to know when the two equations might
    # have integer solutions so we use the diophantine
    # solver
    va, vb = diop_linear(eq(r1, Dummy('a')) - eq(r2, Dummy('b')))

    # check for no solution
    no_solution = va is None and vb is None
    if no_solution:
        return S.EmptySet

    # there is a solution
    # -------------------

    # find the coincident point, c
    a0 = va.as_coeff_Add()[0]
    c = eq(r1, a0)

    # find the first point, if possible, in each range
    # since c may not be that point
    def _first_finite_point(r1, c):
        if c == r1.start:
            return c
        # st is the signed step we need to take to
        # get from c to r1.start
        st = sign(r1.start - c)*step
        # use Range to calculate the first point:
        # we want to get as close as possible to
        # r1.start; the Range will not be null since
        # it will at least contain c
        s1 = Range(c, r1.start + st, st)[-1]
        if s1 == r1.start:
            pass
        else:
            # if we didn't hit r1.start then, if the
            # sign of st didn't match the sign of r1.step
            # we are off by one and s1 is not in r1
            if sign(r1.step) != sign(st):
                s1 -= st
        if s1 not in r1:
            return
        return s1

    # calculate the step size of the new Range
    step = abs(ilcm(r1.step, r2.step))
    s1 = _first_finite_point(r1, c)
    if s1 is None:
        return S.EmptySet
    s2 = _first_finite_point(r2, c)
    if s2 is None:
        return S.EmptySet

    # replace the corresponding start or stop in
    # the original Ranges with these points; the
    # result must have at least one point since
    # we know that s1 and s2 are in the Ranges
    def _updated_range(r, first):
        st = sign(r.step)*step
        if r.start.is_finite:
            rv = Range(first, r.stop, st)
        else:
            rv = Range(r.start, first + st, st)
        return rv
    r1 = _updated_range(a, s1)
    r2 = _updated_range(b, s2)

    # work with them both in the increasing direction
    if sign(r1.step) < 0:
        r1 = r1.reversed
    if sign(r2.step) < 0:
        r2 = r2.reversed

    # return clipped Range with positive step; it
    # can't be empty at this point
    start = max(r1.start, r2.start)
    stop = min(r1.stop, r2.stop)
    return Range(start, stop, step)


def _(a, b):
    return a


def _(a, b):
    return a


def _(self, other):
    from sympy.solvers.diophantine import diophantine

    # Only handle the straight-forward univariate case
    if (len(self.lamda.variables) > 1
            or self.lamda.signature != self.lamda.variables):
        return None
    base_set = self.base_sets[0]

    # Intersection between ImageSets with Integers as base set
    # For {f(n) : n in Integers} & {g(m) : m in Integers} we solve the
    # diophantine equations f(n)=g(m).
    # If the solutions for n are {h(t) : t in Integers} then we return
    # {f(h(t)) : t in integers}.
    # If the solutions for n are {n_1, n_2, ..., n_k} then we return
    # {f(n_i) : 1 <= i <= k}.
    if base_set is S.Integers:
        gm = None
        if isinstance(other, ImageSet) and other.base_sets == (S.Integers,):
            gm = other.lamda.expr
            var = other.lamda.variables[0]
            # Symbol of second ImageSet lambda must be distinct from first
            m = Dummy('m')
            gm = gm.subs(var, m)
        elif other is S.Integers:
            m = gm = Dummy('m')
        if gm is not None:
            fn = self.lamda.expr
            n = self.lamda.variables[0]
            try:
                solns = list(diophantine(fn - gm, syms=(n, m), permute=True))
            except (TypeError, NotImplementedError):
                # TypeError if equation not polynomial with rational coeff.
                # NotImplementedError if correct format but no solver.
                return
            # 3 cases are possible for solns:
            # - empty set,
            # - one or more parametric (infinite) solutions,
            # - a finite number of (non-parametric) solution couples.
            # Among those, there is one type of solution set that is
            # not helpful here: multiple parametric solutions.
            if len(solns) == 0:
                return S.EmptySet
            elif any(s.free_symbols for tupl in solns for s in tupl):
                if len(solns) == 1:
                    soln, solm = solns[0]
                    (t,) = soln.free_symbols
                    expr = fn.subs(n, soln.subs(t, n)).expand()
                    return imageset(Lambda(n, expr), S.Integers)
                else:
                    return
            else:
                return FiniteSet(*(fn.subs(n, s[0]) for s in solns))

    if other == S.Reals:
        from sympy.solvers.solvers import denoms, solve_linear

        def _solution_union(exprs, sym):
            # return a union of linear solutions to i in expr;
            # if i cannot be solved, use a ConditionSet for solution
            sols = []
            for i in exprs:
                x, xis = solve_linear(i, 0, [sym])
                if x == sym:
                    sols.append(FiniteSet(xis))
                else:
                    sols.append(ConditionSet(sym, Eq(i, 0)))
            return Union(*sols)

        f = self.lamda.expr
        n = self.lamda.variables[0]

        n_ = Dummy(n.name, real=True)
        f_ = f.subs(n, n_)

        re, im = f_.as_real_imag()
        im = expand_complex(im)

        re = re.subs(n_, n)
        im = im.subs(n_, n)
        ifree = im.free_symbols
        lam = Lambda(n, re)
        if im.is_zero:
            # allow re-evaluation
            # of self in this case to make
            # the result canonical
            pass
        elif im.is_zero is False:
            return S.EmptySet
        elif ifree != {n}:
            return None
        else:
            # univarite imaginary part in same variable;
            # use numer instead of as_numer_denom to keep
            # this as fast as possible while still handling
            # simple cases
            base_set &= _solution_union(
                Mul.make_args(numer(im)), n)
        # exclude values that make denominators 0
        base_set -= _solution_union(denoms(f), n)
        return imageset(lam, base_set)

    elif isinstance(other, Interval):
        from sympy.solvers.solveset import (invert_real, invert_complex,
                                            solveset)

        f = self.lamda.expr
        n = self.lamda.variables[0]
        new_inf, new_sup = None, None
        new_lopen, new_ropen = other.left_open, other.right_open

        if f.is_real:
            inverter = invert_real
        else:
            inverter = invert_complex

        g1, h1 = inverter(f, other.inf, n)
        g2, h2 = inverter(f, other.sup, n)

        if all(isinstance(i, FiniteSet) for i in (h1, h2)):
            if g1 == n:
                if len(h1) == 1:
                    new_inf = h1.args[0]
            if g2 == n:
                if len(h2) == 1:
                    new_sup = h2.args[0]
            # TODO: Design a technique to handle multiple-inverse
            # functions

            # Any of the new boundary values cannot be determined
            if any(i is None for i in (new_sup, new_inf)):
                return


            range_set = S.EmptySet

            if all(i.is_real for i in (new_sup, new_inf)):
                # this assumes continuity of underlying function
                # however fixes the case when it is decreasing
                if new_inf > new_sup:
                    new_inf, new_sup = new_sup, new_inf
                new_interval = Interval(new_inf, new_sup, new_lopen, new_ropen)
                range_set = base_set.intersect(new_interval)
            else:
                if other.is_subset(S.Reals):
                    solutions = solveset(f, n, S.Reals)
                    if not isinstance(range_set, (ImageSet, ConditionSet)):
                        range_set = solutions.intersect(other)
                    else:
                        return

            if range_set is S.EmptySet:
                return S.EmptySet
            elif isinstance(range_set, Range) and range_set.size is not S.Infinity:
                range_set = FiniteSet(*list(range_set))

            if range_set is not None:
                return imageset(Lambda(n, f), range_set)
            return
        else:
            return


def _(a, b):
    if len(b.args) != len(a.args):
        return S.EmptySet
    return ProductSet(*(i.intersect(j) for i, j in zip(a.sets, b.sets)))


def _(a, b):
    # handle (-oo, oo)
    infty = S.NegativeInfinity, S.Infinity
    if a == Interval(*infty):
        l, r = a.left, a.right
        if l.is_real or l in infty or r.is_real or r in infty:
            return b

    # We can't intersect [0,3] with [x,6] -- we don't know if x>0 or x<0
    if not a._is_comparable(b):
        return None

    empty = False

    if a.start <= b.end and b.start <= a.end:
        # Get topology right.
        if a.start < b.start:
            start = b.start
            left_open = b.left_open
        elif a.start > b.start:
            start = a.start
            left_open = a.left_open
        else:
            start = a.start
            if not _aresame(a.start, b.start):
                # For example Integer(2) != Float(2)
                # Prefer the Float boundary because Floats should be
                # contagious in calculations.
                if b.start.has(Float) and not a.start.has(Float):
                    start = b.start
                elif a.start.has(Float) and not b.start.has(Float):
                    start = a.start
                else:
                    #this is to ensure that if Eq(a.start, b.start) but
                    #type(a.start) != type(b.start) the order of a and b
                    #does not matter for the result
                    start = list(ordered([a,b]))[0].start
            left_open = a.left_open or b.left_open

        if a.end < b.end:
            end = a.end
            right_open = a.right_open
        elif a.end > b.end:
            end = b.end
            right_open = b.right_open
        else:
            # see above for logic with start
            end = a.end
            if not _aresame(a.end, b.end):
                if b.end.has(Float) and not a.end.has(Float):
                    end = b.end
                elif a.end.has(Float) and not b.end.has(Float):
                    end = a.end
                else:
                    end = list(ordered([a,b]))[0].end
            right_open = a.right_open or b.right_open

        if end - start == 0 and (left_open or right_open):
            empty = True
    else:
        empty = True

    if empty:
        return S.EmptySet

    return Interval(start, end, left_open, right_open)


def _(a, b):
    return S.EmptySet


def _(a, b):
    return b


def _(a, b):
    return FiniteSet(*(a._elements & b._elements))


def _(a, b):
    try:
        return FiniteSet(*[el for el in a if el in b])
    except TypeError:
        return None  # could not evaluate `el in b` due to symbolic ranges.


def _(a, b):
    return None


def _(a, b):
    return a


def _(a, b):
    return a


def _(a, b):
    return a


def _(a, b):
    return _intlike_interval(a, b)


def _(a, b):
    return _intlike_interval(a, b)


def _(a, b):
    return None


def _(a, b):
    # This is correct but can be made more comprehensive...
    if fuzzy_bool(a.start < b.start):
        return False
    if fuzzy_bool(a.end > b.end):
        return False
    if (b.left_open and not a.left_open and fuzzy_bool(Eq(a.start, b.start))):
        return False
    if (b.right_open and not a.right_open and fuzzy_bool(Eq(a.end, b.end))):
        return False


def _(a_interval, b_fs):
    # An Interval can only be a subset of a finite set if it is finite
    # which can only happen if it has zero measure.
    if fuzzy_not(a_interval.measure.is_zero):
        return False


def _(a_interval, b_u):
    if all(isinstance(s, (Interval, FiniteSet)) for s in b_u.args):
        intervals = [s for s in b_u.args if isinstance(s, Interval)]
        if all(fuzzy_bool(a_interval.start < s.start) for s in intervals):
            return False
        if all(fuzzy_bool(a_interval.end > s.end) for s in intervals):
            return False
        if a_interval.measure.is_nonzero:
            no_overlap = lambda s1, s2: fuzzy_or([
                    fuzzy_bool(s1.end <= s2.start),
                    fuzzy_bool(s1.start >= s2.end),
                    ])
            if all(no_overlap(s, a_interval) for s in intervals):
                return False


def _(a, b):
    if a.step == b.step == 1:
        return fuzzy_and([fuzzy_bool(a.start >= b.start),
                          fuzzy_bool(a.stop <= b.stop)])


def _(a_range, b_interval):
    if a_range.step.is_positive:
        if b_interval.left_open and a_range.inf.is_finite:
            cond_left = a_range.inf > b_interval.left
        else:
            cond_left = a_range.inf >= b_interval.left
        if b_interval.right_open and a_range.sup.is_finite:
            cond_right = a_range.sup < b_interval.right
        else:
            cond_right = a_range.sup <= b_interval.right
        return fuzzy_and([cond_left, cond_right])


def _(a_range, b_finiteset):
    try:
        a_size = a_range.size
    except ValueError:
        # symbolic Range of unknown size
        return None
    if a_size > len(b_finiteset):
        return False
    elif any(arg.has(Symbol) for arg in a_range.args):
        return fuzzy_and(b_finiteset.contains(x) for x in a_range)
    else:
        # Checking A \ B == EmptySet is more efficient than repeated naive
        # membership checks on an arbitrary FiniteSet.
        a_set = set(a_range)
        b_remaining = len(b_finiteset)
        # Symbolic expressions and numbers of unknown type (integer or not) are
        # all counted as "candidates", i.e. *potentially* matching some a in
        # a_range.
        cnt_candidate = 0
        for b in b_finiteset:
            if b.is_Integer:
                a_set.discard(b)
            elif fuzzy_not(b.is_integer):
                pass
            else:
                cnt_candidate += 1
            b_remaining -= 1
            if len(a_set) > b_remaining + cnt_candidate:
                return False
            if len(a_set) == 0:
                return True
        return None


def _(a_interval, b_range):
    if a_interval.measure.is_extended_nonzero:
        return False


def _(a_interval, b_rationals):
    if a_interval.measure.is_extended_nonzero:
        return False


def _(a, b):
    return True


def _(a, b):
    return False


def _(a, b):
    return False


def _(a, b):
    return False


def _(a, b):
    return True


def _(a, b):
    return False


def _(a_ps, b_fs):
    return fuzzy_and(b_fs.contains(x) for x in a_ps)


def _(x, y):
    return None


def _(x, y):
    return None


def _(x, y):
    return x*y


def _(x, y):
    """
    Multiplications in interval arithmetic
    https://en.wikipedia.org/wiki/Interval_arithmetic
    """
    # TODO: some intervals containing 0 and oo will fail as 0*oo returns nan.
    comvals = (
        (x.start * y.start, bool(x.left_open or y.left_open)),
        (x.start * y.end, bool(x.left_open or y.right_open)),
        (x.end * y.start, bool(x.right_open or y.left_open)),
        (x.end * y.end, bool(x.right_open or y.right_open)),
    )
    # TODO: handle symbolic intervals
    minval, minopen = min(comvals)
    maxval, maxopen = max(comvals)
    return Interval(
        minval,
        maxval,
        minopen,
        maxopen
    )


def _(x, y):
    return None


def _(x, y):
    return x/y


def _(x, y):
    return None


def _(x, y):
    """
    Divisions in interval arithmetic
    https://en.wikipedia.org/wiki/Interval_arithmetic
    """
    if (y.start*y.end).is_negative:
        return Interval(-oo, oo)
    if y.start == 0:
        s2 = oo
    else:
        s2 = 1/y.start
    if y.end == 0:
        s1 = -oo
    else:
        s1 = 1/y.end
    return set_mul(x, Interval(s1, s2, y.right_open, y.left_open))


def _(x, y):
    return None


def _(x, y):
    return ImageSet(Lambda((_x, _y), (_x ** _y)), x, y)


def _(x, y):
    return x**y


def _(x, z):
    return FiniteSet(S.One)


def _(x, exponent):
    """
    Powers in interval arithmetic
    https://en.wikipedia.org/wiki/Interval_arithmetic
    """
    s1 = x.start**exponent
    s2 = x.end**exponent
    if ((s2 > s1) if exponent > 0 else (x.end > -x.start)) == True:
        left_open = x.left_open
        right_open = x.right_open
        # TODO: handle unevaluated condition.
        sleft = s2
    else:
        # TODO: `s2 > s1` could be unevaluated.
        left_open = x.right_open
        right_open = x.left_open
        sleft = s1

    if x.start.is_positive:
        return Interval(
            Min(s1, s2),
            Max(s1, s2), left_open, right_open)
    elif x.end.is_negative:
        return Interval(
            Min(s1, s2),
            Max(s1, s2), left_open, right_open)

    # Case where x.start < 0 and x.end > 0:
    if exponent.is_odd:
        if exponent.is_negative:
            if x.start.is_zero:
                return Interval(s2, oo, x.right_open)
            if x.end.is_zero:
                return Interval(-oo, s1, True, x.left_open)
            return Union(Interval(-oo, s1, True, x.left_open), Interval(s2, oo, x.right_open))
        else:
            return Interval(s1, s2, x.left_open, x.right_open)
    elif exponent.is_even:
        if exponent.is_negative:
            if x.start.is_zero:
                return Interval(s2, oo, x.right_open)
            if x.end.is_zero:
                return Interval(s1, oo, x.left_open)
            return Interval(0, oo)
        else:
            return Interval(S.Zero, sleft, S.Zero not in x, left_open)


def _(b, e):
    # TODO: add logic for open intervals?
    if b.start.is_nonnegative:
        if b.end < 1:
            return FiniteSet(S.Zero)
        if b.start > 1:
            return FiniteSet(S.Infinity)
        return Interval(0, oo)
    elif b.end.is_negative:
        if b.start > -1:
            return FiniteSet(S.Zero)
        if b.end < -1:
            return FiniteSet(-oo, oo)
        return Interval(-oo, oo)
    else:
        if b.start > -1:
            if b.end < 1:
                return FiniteSet(S.Zero)
            return Interval(0, oo)
        return Interval(-oo, oo)


def _(b, e):
    return _set_pow(set_div(S.One, b), oo)


def _(a, b):
    return a


def _(a, b):
    return a


def _(a, b):
    return a


def _(a, b):
    return a


def _(a, b):
    return a


def _(a, b):
    return a


def _(a, b):
    intersect = Intersection(a, b)
    if intersect == a:
        return b
    elif intersect == b:
        return a


def _(a, b):
    if b.is_subset(S.Reals):
        # treat a subset of reals as a complex region
        b = ComplexRegion.from_real(b)

    if b.is_ComplexRegion:
        # a in rectangular form
        if (not a.polar) and (not b.polar):
            return ComplexRegion(Union(a.sets, b.sets))
        # a in polar form
        elif a.polar and b.polar:
            return ComplexRegion(Union(a.sets, b.sets), polar=True)
    return None


def _(a, b):
    return b


def _(a, b):
    return a


def _(a, b):
    if b.is_subset(a):
        return a
    if len(b.sets) != len(a.sets):
        return None
    if len(a.sets) == 2:
        a1, a2 = a.sets
        b1, b2 = b.sets
        if a1 == b1:
            return a1 * Union(a2, b2)
        if a2 == b2:
            return Union(a1, b1) * a2
    return None


def _(a, b):
    if b.is_subset(a):
        return a
    return None


def _(a, b):
    if a._is_comparable(b):
        # Non-overlapping intervals
        end = Min(a.end, b.end)
        start = Max(a.start, b.start)
        if (end < start or
           (end == start and (end not in a and end not in b))):
            return None
        else:
            start = Min(a.start, b.start)
            end = Max(a.end, b.end)

            left_open = ((a.start != start or a.left_open) and
                         (b.start != start or b.left_open))
            right_open = ((a.end != end or a.right_open) and
                          (b.end != end or b.right_open))
            return Interval(start, end, left_open, right_open)


def _(a, b):
    return S.UniversalSet


def _(a, b):
    # If I have open end points and these endpoints are contained in b
    # But only in case, when endpoints are finite. Because
    # interval does not contain oo or -oo.
    open_left_in_b_and_finite = (a.left_open and
                                     sympify(b.contains(a.start)) is S.true and
                                     a.start.is_finite)
    open_right_in_b_and_finite = (a.right_open and
                                      sympify(b.contains(a.end)) is S.true and
                                      a.end.is_finite)
    if open_left_in_b_and_finite or open_right_in_b_and_finite:
        # Fill in my end points and return
        open_left = a.left_open and a.start not in b
        open_right = a.right_open and a.end not in b
        new_a = Interval(a.start, a.end, open_left, open_right)
        return {new_a, b}
    return None


def _(a, b):
    return FiniteSet(*(a._elements | b._elements))


def _(a, b):
    # If `b` set contains one of my elements, remove it from `a`
    if any(b.contains(x) == True for x in a):
        return {
            FiniteSet(*[x for x in a if b.contains(x) != True]), b}
    return None


def _(a, b):
    return None


def _(expr, assumptions):
    """
    Handles Symbol.
    """
    if expr.is_finite is not None:
        return expr.is_finite
    if Q.finite(expr) in conjuncts(assumptions):
        return True
    return None


def _(expr, assumptions):
    """
    Return True if expr is bounded, False if not and None if unknown.

    Truth Table:

    +-------+-----+-----------+-----------+
    |       |     |           |           |
    |       |  B  |     U     |     ?     |
    |       |     |           |           |
    +-------+-----+---+---+---+---+---+---+
    |       |     |   |   |   |   |   |   |
    |       |     |'+'|'-'|'x'|'+'|'-'|'x'|
    |       |     |   |   |   |   |   |   |
    +-------+-----+---+---+---+---+---+---+
    |       |     |           |           |
    |   B   |  B  |     U     |     ?     |
    |       |     |           |           |
    +---+---+-----+---+---+---+---+---+---+
    |   |   |     |   |   |   |   |   |   |
    |   |'+'|     | U | ? | ? | U | ? | ? |
    |   |   |     |   |   |   |   |   |   |
    |   +---+-----+---+---+---+---+---+---+
    |   |   |     |   |   |   |   |   |   |
    | U |'-'|     | ? | U | ? | ? | U | ? |
    |   |   |     |   |   |   |   |   |   |
    |   +---+-----+---+---+---+---+---+---+
    |   |   |     |           |           |
    |   |'x'|     |     ?     |     ?     |
    |   |   |     |           |           |
    +---+---+-----+---+---+---+---+---+---+
    |       |     |           |           |
    |   ?   |     |           |     ?     |
    |       |     |           |           |
    +-------+-----+-----------+---+---+---+

        * 'B' = Bounded

        * 'U' = Unbounded

        * '?' = unknown boundedness

        * '+' = positive sign

        * '-' = negative sign

        * 'x' = sign unknown

        * All Bounded -> True

        * 1 Unbounded and the rest Bounded -> False

        * >1 Unbounded, all with same known sign -> False

        * Any Unknown and unknown sign -> None

        * Else -> None

    When the signs are not the same you can have an undefined
    result as in oo - oo, hence 'bounded' is also undefined.
    """
    sign = -1  # sign of unknown or infinite
    result = True
    for arg in expr.args:
        _bounded = ask(Q.finite(arg), assumptions)
        if _bounded:
            continue
        s = ask(Q.extended_positive(arg), assumptions)
        # if there has been more than one sign or if the sign of this arg
        # is None and Bounded is None or there was already
        # an unknown sign, return None
        if sign != -1 and s != sign or \
                s is None and None in (_bounded, sign):
            return None
        else:
            sign = s
        # once False, do not change
        if result is not False:
            result = _bounded
    return result


def _(expr, assumptions):
    """
    Return True if expr is bounded, False if not and None if unknown.

    Truth Table:

    +---+---+---+--------+
    |   |   |   |        |
    |   | B | U |   ?    |
    |   |   |   |        |
    +---+---+---+---+----+
    |   |   |   |   |    |
    |   |   |   | s | /s |
    |   |   |   |   |    |
    +---+---+---+---+----+
    |   |   |   |        |
    | B | B | U |   ?    |
    |   |   |   |        |
    +---+---+---+---+----+
    |   |   |   |   |    |
    | U |   | U | U | ?  |
    |   |   |   |   |    |
    +---+---+---+---+----+
    |   |   |   |        |
    | ? |   |   |   ?    |
    |   |   |   |        |
    +---+---+---+---+----+

        * B = Bounded

        * U = Unbounded

        * ? = unknown boundedness

        * s = signed (hence nonzero)

        * /s = not signed
    """
    result = True
    possible_zero = False
    for arg in expr.args:
        _bounded = ask(Q.finite(arg), assumptions)
        if _bounded:
            if ask(Q.zero(arg), assumptions) is not False:
                if result is False:
                    return None
                possible_zero = True
        elif _bounded is None:
            if result is None:
                return None
            if ask(Q.extended_nonzero(arg), assumptions) is None:
                return None
            if result is not False:
                result = None
        else:
            if possible_zero:
                return None
            result = False
    return result


def _(expr, assumptions):
    """
    * Unbounded ** NonZero -> Unbounded

    * Bounded ** Bounded -> Bounded

    * Abs()<=1 ** Positive -> Bounded

    * Abs()>=1 ** Negative -> Bounded

    * Otherwise unknown
    """
    if expr.base == E:
        return ask(Q.finite(expr.exp), assumptions)

    base_bounded = ask(Q.finite(expr.base), assumptions)
    exp_bounded = ask(Q.finite(expr.exp), assumptions)
    if base_bounded is None and exp_bounded is None:  # Common Case
        return None
    if base_bounded is False and ask(Q.extended_nonzero(expr.exp), assumptions):
        return False
    if base_bounded and exp_bounded:
        is_base_zero = ask(Q.zero(expr.base),assumptions)
        is_exp_negative = ask(Q.negative(expr.exp),assumptions)
        if is_base_zero is True and is_exp_negative is True:
            return False
        if is_base_zero is not False and is_exp_negative is not False:
            return None
        return True
    if (abs(expr.base) <= 1) == True and ask(Q.extended_positive(expr.exp), assumptions):
        return True
    if (abs(expr.base) >= 1) == True and ask(Q.extended_negative(expr.exp), assumptions):
        return True
    if (abs(expr.base) >= 1) == True and exp_bounded is False:
        return False
    return None


def _(expr, assumptions):
    return ask(Q.finite(expr.exp), assumptions)


def _(expr, assumptions):
    # After complex -> finite fact is registered to new assumption system,
    # querying Q.infinite may be removed.
    if ask(Q.infinite(expr.args[0]), assumptions):
        return False
    return ask(~Q.zero(expr.args[0]), assumptions)


def _(expr, assumptions):
    return True


def _(expr, assumptions):
    return False


def _(expr, assumptions):
    return None


def _(expr, assumptions):
    is_finite = Q.finite(expr)._eval_ask(assumptions)
    if is_finite is None:
        return None
    return not is_finite


def _(expr, assumptions):
    return True


def _(expr, assumptions):
    return False


def _(expr, assumptions):
    return True


def _(expr, assumptions):
    return False


def _(expr, assumptions):
    """Objects are expected to be commutative unless otherwise stated"""
    assumps = conjuncts(assumptions)
    if expr.is_commutative is not None:
        return expr.is_commutative and not ~Q.commutative(expr) in assumps
    if Q.commutative(expr) in assumps:
        return True
    elif ~Q.commutative(expr) in assumps:
        return False
    return True


def _(expr, assumptions):
    for arg in expr.args:
        if not ask(Q.commutative(arg), assumptions):
            return False
    return True


def _(expr, assumptions):
    return True


def _(expr, assumptions):
    return True


def _(expr, assumptions):
    return expr


def _(expr, assumptions):
    return True


def _(expr, assumptions):
    return False


def _(expr, assumptions):
    return ask(expr, assumptions)


def _(expr, assumptions):
    arg = expr.args[0]
    if arg.is_Symbol:
        # symbol used as abstract boolean object
        return None
    value = ask(arg, assumptions=assumptions)
    if value in (True, False):
        return not value
    else:
        return None


def _(expr, assumptions):
    result = False
    for arg in expr.args:
        p = ask(arg, assumptions=assumptions)
        if p is True:
            return True
        if p is None:
            result = None
    return result


def _(expr, assumptions):
    result = True
    for arg in expr.args:
        p = ask(arg, assumptions=assumptions)
        if p is False:
            return False
        if p is None:
            result = None
    return result


def _(expr, assumptions):
    p, q = expr.args
    return ask(~p | q, assumptions=assumptions)


def _(expr, assumptions):
    p, q = expr.args
    pt = ask(p, assumptions=assumptions)
    if pt is None:
        return None
    qt = ask(q, assumptions=assumptions)
    if qt is None:
        return None
    return pt == qt


def _(expr, assumptions):
    return expr.shape[0] == expr.shape[1]


def _(expr, assumptions):
    factor, mmul = expr.as_coeff_mmul()
    if all(ask(Q.symmetric(arg), assumptions) for arg in mmul.args):
        return True
    # TODO: implement sathandlers system for the matrices.
    # Now it duplicates the general fact: Implies(Q.diagonal, Q.symmetric).
    if ask(Q.diagonal(expr), assumptions):
        return True
    if len(mmul.args) >= 2 and mmul.args[0] == mmul.args[-1].T:
        if len(mmul.args) == 2:
            return True
        return ask(Q.symmetric(MatMul(*mmul.args[1:-1])), assumptions)


def _(expr, assumptions):
    # only for integer powers
    base, exp = expr.args
    int_exp = ask(Q.integer(exp), assumptions)
    if not int_exp:
        return None
    non_negative = ask(~Q.negative(exp), assumptions)
    if (non_negative or non_negative == False
                        and ask(Q.invertible(base), assumptions)):
        return ask(Q.symmetric(base), assumptions)
    return None


def _(expr, assumptions):
    return all(ask(Q.symmetric(arg), assumptions) for arg in expr.args)


def _(expr, assumptions):
    if not expr.is_square:
        return False
    # TODO: implement sathandlers system for the matrices.
    # Now it duplicates the general fact: Implies(Q.diagonal, Q.symmetric).
    if ask(Q.diagonal(expr), assumptions):
        return True
    if Q.symmetric(expr) in conjuncts(assumptions):
        return True


def _(expr, assumptions):
    return ask(Q.square(expr), assumptions)


def _(expr, assumptions):
    return ask(Q.symmetric(expr.arg), assumptions)


def _(expr, assumptions):
    # TODO: implement sathandlers system for the matrices.
    # Now it duplicates the general fact: Implies(Q.diagonal, Q.symmetric).
    if ask(Q.diagonal(expr), assumptions):
        return True
    if not expr.on_diag:
        return None
    else:
        return ask(Q.symmetric(expr.parent), assumptions)


def _(expr, assumptions):
    return True


def _(expr, assumptions):
    factor, mmul = expr.as_coeff_mmul()
    if all(ask(Q.invertible(arg), assumptions) for arg in mmul.args):
        return True
    if any(ask(Q.invertible(arg), assumptions) is False
            for arg in mmul.args):
        return False


def _(expr, assumptions):
    # only for integer powers
    base, exp = expr.args
    int_exp = ask(Q.integer(exp), assumptions)
    if not int_exp:
        return None
    if exp.is_negative == False:
        return ask(Q.invertible(base), assumptions)
    return None


def _(expr, assumptions):
    return None


def _(expr, assumptions):
    if not expr.is_square:
        return False
    if Q.invertible(expr) in conjuncts(assumptions):
        return True


def _(expr, assumptions):
    return True


def _(expr, assumptions):
    return False


def _(expr, assumptions):
    return expr.shape[0] == 1 and expr.shape[1] == 1


def _(expr, assumptions):
    return ask(Q.invertible(expr.arg), assumptions)


def _(expr, assumptions):
    if not expr.on_diag:
        return None
    else:
        return ask(Q.invertible(expr.parent), assumptions)


def _(expr, assumptions):
    if not expr.is_square:
        return False
    return expr.rank() == expr.rows


def _(expr, assumptions):
    if not expr.is_square:
        return False
    return None


def _(expr, assumptions):
    if not expr.is_square:
        return False
    if expr.blockshape == (1, 1):
        return ask(Q.invertible(expr.blocks[0, 0]), assumptions)
    expr = reblock_2x2(expr)
    if expr.blockshape == (2, 2):
        [[A, B], [C, D]] = expr.blocks.tolist()
        if ask(Q.invertible(A), assumptions) == True:
            invertible = ask(Q.invertible(D - C * A.I * B), assumptions)
            if invertible is not None:
                return invertible
        if ask(Q.invertible(B), assumptions) == True:
            invertible = ask(Q.invertible(C - D * B.I * A), assumptions)
            if invertible is not None:
                return invertible
        if ask(Q.invertible(C), assumptions) == True:
            invertible = ask(Q.invertible(B - A * C.I * D), assumptions)
            if invertible is not None:
                return invertible
        if ask(Q.invertible(D), assumptions) == True:
            invertible = ask(Q.invertible(A - B * D.I * C), assumptions)
            if invertible is not None:
                return invertible
    return None


def _(expr, assumptions):
    if expr.rowblocksizes != expr.colblocksizes:
        return None
    return fuzzy_and([ask(Q.invertible(a), assumptions) for a in expr.diag])


def _(expr, assumptions):
    factor, mmul = expr.as_coeff_mmul()
    if (all(ask(Q.orthogonal(arg), assumptions) for arg in mmul.args) and
            factor == 1):
        return True
    if any(ask(Q.invertible(arg), assumptions) is False
            for arg in mmul.args):
        return False


def _(expr, assumptions):
    # only for integer powers
    base, exp = expr.args
    int_exp = ask(Q.integer(exp), assumptions)
    if int_exp:
        return ask(Q.orthogonal(base), assumptions)
    return None


def _(expr, assumptions):
    if (len(expr.args) == 1 and
            ask(Q.orthogonal(expr.args[0]), assumptions)):
        return True


def _(expr, assumptions):
    if (not expr.is_square or
                    ask(Q.invertible(expr), assumptions) is False):
        return False
    if Q.orthogonal(expr) in conjuncts(assumptions):
        return True


def _(expr, assumptions):
    return True


def _(expr, assumptions):
    return False


def _(expr, assumptions):
    return ask(Q.orthogonal(expr.arg), assumptions)


def _(expr, assumptions):
    if not expr.on_diag:
        return None
    else:
        return ask(Q.orthogonal(expr.parent), assumptions)


def _(expr, assumptions):
    return _Factorization(Q.orthogonal, expr, assumptions)


def _(expr, assumptions):
    factor, mmul = expr.as_coeff_mmul()
    if (all(ask(Q.unitary(arg), assumptions) for arg in mmul.args) and
            abs(factor) == 1):
        return True
    if any(ask(Q.invertible(arg), assumptions) is False
            for arg in mmul.args):
        return False


def _(expr, assumptions):
    # only for integer powers
    base, exp = expr.args
    int_exp = ask(Q.integer(exp), assumptions)
    if int_exp:
        return ask(Q.unitary(base), assumptions)
    return None


def _(expr, assumptions):
    if (not expr.is_square or
                    ask(Q.invertible(expr), assumptions) is False):
        return False
    if Q.unitary(expr) in conjuncts(assumptions):
        return True


def _(expr, assumptions):
    return ask(Q.unitary(expr.arg), assumptions)


def _(expr, assumptions):
    if not expr.on_diag:
        return None
    else:
        return ask(Q.unitary(expr.parent), assumptions)


def _(expr, assumptions):
    return True


def _(expr, assumptions):
    return False


def _(expr, assumptions):
    return _Factorization(Q.unitary, expr, assumptions)


def _(expr, assumptions):
    if all(ask(Q.fullrank(arg), assumptions) for arg in expr.args):
        return True


def _(expr, assumptions):
    # only for integer powers
    base, exp = expr.args
    int_exp = ask(Q.integer(exp), assumptions)
    if int_exp and ask(~Q.negative(exp), assumptions):
        return ask(Q.fullrank(base), assumptions)
    return None


def _(expr, assumptions):
    return True


def _(expr, assumptions):
    return False


def _(expr, assumptions):
    return expr.shape[0] == 1 and expr.shape[1] == 1


def _(expr, assumptions):
    return ask(Q.fullrank(expr.arg), assumptions)


def _(expr, assumptions):
    if ask(Q.orthogonal(expr.parent), assumptions):
        return True


def _(expr, assumptions):
    factor, mmul = expr.as_coeff_mmul()
    if (all(ask(Q.positive_definite(arg), assumptions)
            for arg in mmul.args) and factor > 0):
        return True
    if (len(mmul.args) >= 2
            and mmul.args[0] == mmul.args[-1].T
            and ask(Q.fullrank(mmul.args[0]), assumptions)):
        return ask(Q.positive_definite(
            MatMul(*mmul.args[1:-1])), assumptions)


def _(expr, assumptions):
    # a power of a positive definite matrix is positive definite
    if ask(Q.positive_definite(expr.args[0]), assumptions):
        return True


def _(expr, assumptions):
    if all(ask(Q.positive_definite(arg), assumptions)
            for arg in expr.args):
        return True


def _(expr, assumptions):
    if not expr.is_square:
        return False
    if Q.positive_definite(expr) in conjuncts(assumptions):
        return True


def _(expr, assumptions):
    return True


def _(expr, assumptions):
    return False


def _(expr, assumptions):
    return expr.shape[0] == 1 and expr.shape[1] == 1


def _(expr, assumptions):
    return ask(Q.positive_definite(expr.arg), assumptions)


def _(expr, assumptions):
    if not expr.on_diag:
        return None
    else:
        return ask(Q.positive_definite(expr.parent), assumptions)


def _(expr, assumptions):
    factor, matrices = expr.as_coeff_matrices()
    if all(ask(Q.upper_triangular(m), assumptions) for m in matrices):
        return True


def _(expr, assumptions):
    if all(ask(Q.upper_triangular(arg), assumptions) for arg in expr.args):
        return True


def _(expr, assumptions):
    # only for integer powers
    base, exp = expr.args
    int_exp = ask(Q.integer(exp), assumptions)
    if not int_exp:
        return None
    non_negative = ask(~Q.negative(exp), assumptions)
    if (non_negative or non_negative == False
                        and ask(Q.invertible(base), assumptions)):
        return ask(Q.upper_triangular(base), assumptions)
    return None


def _(expr, assumptions):
    if Q.upper_triangular(expr) in conjuncts(assumptions):
        return True


def _(expr, assumptions):
    return True


def _(expr, assumptions):
    return expr.shape[0] == 1 and expr.shape[1] == 1


def _(expr, assumptions):
    return ask(Q.lower_triangular(expr.arg), assumptions)


def _(expr, assumptions):
    return ask(Q.upper_triangular(expr.arg), assumptions)


def _(expr, assumptions):
    if not expr.on_diag:
        return None
    else:
        return ask(Q.upper_triangular(expr.parent), assumptions)


def _(expr, assumptions):
    return _Factorization(Q.upper_triangular, expr, assumptions)


def _(expr, assumptions):
    factor, matrices = expr.as_coeff_matrices()
    if all(ask(Q.lower_triangular(m), assumptions) for m in matrices):
        return True


def _(expr, assumptions):
    if all(ask(Q.lower_triangular(arg), assumptions) for arg in expr.args):
        return True


def _(expr, assumptions):
    # only for integer powers
    base, exp = expr.args
    int_exp = ask(Q.integer(exp), assumptions)
    if not int_exp:
        return None
    non_negative = ask(~Q.negative(exp), assumptions)
    if (non_negative or non_negative == False
                        and ask(Q.invertible(base), assumptions)):
        return ask(Q.lower_triangular(base), assumptions)
    return None


def _(expr, assumptions):
    if Q.lower_triangular(expr) in conjuncts(assumptions):
        return True


def _(expr, assumptions):
    return True


def _(expr, assumptions):
    return expr.shape[0] == 1 and expr.shape[1] == 1


def _(expr, assumptions):
    return ask(Q.upper_triangular(expr.arg), assumptions)


def _(expr, assumptions):
    return ask(Q.lower_triangular(expr.arg), assumptions)


def _(expr, assumptions):
    if not expr.on_diag:
        return None
    else:
        return ask(Q.lower_triangular(expr.parent), assumptions)


def _(expr, assumptions):
    return _Factorization(Q.lower_triangular, expr, assumptions)


def _(expr, assumptions):
    if _is_empty_or_1x1(expr):
        return True
    factor, matrices = expr.as_coeff_matrices()
    if all(ask(Q.diagonal(m), assumptions) for m in matrices):
        return True


def _(expr, assumptions):
    # only for integer powers
    base, exp = expr.args
    int_exp = ask(Q.integer(exp), assumptions)
    if not int_exp:
        return None
    non_negative = ask(~Q.negative(exp), assumptions)
    if (non_negative or non_negative == False
                        and ask(Q.invertible(base), assumptions)):
        return ask(Q.diagonal(base), assumptions)
    return None


def _(expr, assumptions):
    if all(ask(Q.diagonal(arg), assumptions) for arg in expr.args):
        return True


def _(expr, assumptions):
    if _is_empty_or_1x1(expr):
        return True
    if Q.diagonal(expr) in conjuncts(assumptions):
        return True


def _(expr, assumptions):
    return expr.shape[0] == 1 and expr.shape[1] == 1


def _(expr, assumptions):
    return ask(Q.diagonal(expr.arg), assumptions)


def _(expr, assumptions):
    if _is_empty_or_1x1(expr):
        return True
    if not expr.on_diag:
        return None
    else:
        return ask(Q.diagonal(expr.parent), assumptions)


def _(expr, assumptions):
    return True


def _(expr, assumptions):
    return _Factorization(Q.diagonal, expr, assumptions)


def _(expr, assumptions):
    return test_closed_group(expr, assumptions, Q.integer_elements)


def _(expr, assumptions):
    # only for integer powers
    base, exp = expr.args
    int_exp = ask(Q.integer(exp), assumptions)
    if not int_exp:
        return None
    if exp.is_negative == False:
        return ask(Q.integer_elements(base), assumptions)
    return None


def _(expr, assumptions):
    return True


def _(expr, assumptions):
    return MatMul_elements(Q.integer_elements, Q.integer, expr, assumptions)


def _(expr, assumptions):
    return MS_elements(Q.integer_elements, expr, assumptions)


def _(expr, assumptions):
    return BM_elements(Q.integer_elements, expr, assumptions)


def _(expr, assumptions):
    return test_closed_group(expr, assumptions, Q.real_elements)


def _(expr, assumptions):
    # only for integer powers
    base, exp = expr.args
    int_exp = ask(Q.integer(exp), assumptions)
    if not int_exp:
        return None
    non_negative = ask(~Q.negative(exp), assumptions)
    if (non_negative or non_negative == False
                        and ask(Q.invertible(base), assumptions)):
        return ask(Q.real_elements(base), assumptions)
    return None


def _(expr, assumptions):
    return MatMul_elements(Q.real_elements, Q.real, expr, assumptions)


def _(expr, assumptions):
    return MS_elements(Q.real_elements, expr, assumptions)


def _(expr, assumptions):
    return BM_elements(Q.real_elements, expr, assumptions)


def _(expr, assumptions):
    return test_closed_group(expr, assumptions, Q.complex_elements)


def _(expr, assumptions):
    # only for integer powers
    base, exp = expr.args
    int_exp = ask(Q.integer(exp), assumptions)
    if not int_exp:
        return None
    non_negative = ask(~Q.negative(exp), assumptions)
    if (non_negative or non_negative == False
                        and ask(Q.invertible(base), assumptions)):
        return ask(Q.complex_elements(base), assumptions)
    return None


def _(expr, assumptions):
    return MatMul_elements(Q.complex_elements, Q.complex, expr, assumptions)


def _(expr, assumptions):
    return MS_elements(Q.complex_elements, expr, assumptions)


def _(expr, assumptions):
    return BM_elements(Q.complex_elements, expr, assumptions)


def _(expr, assumptions):
    return True


def _(expr, assumptions):
    ret = expr.is_prime
    if ret is None:
        raise MDNotImplementedError
    return ret


def _(expr, assumptions):
    if expr.is_number:
        return _PrimePredicate_number(expr, assumptions)


def _(expr, assumptions):
    if expr.is_number:
        return _PrimePredicate_number(expr, assumptions)
    for arg in expr.args:
        if not ask(Q.integer(arg), assumptions):
            return None
    for arg in expr.args:
        if arg.is_number and arg.is_composite:
            return False


def _(expr, assumptions):
    """
    Integer**Integer     -> !Prime
    """
    if expr.is_number:
        return _PrimePredicate_number(expr, assumptions)
    if ask(Q.integer(expr.exp), assumptions) and \
            ask(Q.integer(expr.base), assumptions):
        prime_base = ask(Q.prime(expr.base), assumptions)
        if prime_base is False:
            return False
        is_exp_one = ask(Q.eq(expr.exp, 1), assumptions)
        if is_exp_one is False:
            return False
        if prime_base is True and is_exp_one is True:
            return True


def _(expr, assumptions):
    return isprime(expr)


def _(expr, assumptions):
    return False


def _(expr, assumptions):
    return _PrimePredicate_number(expr, assumptions)


def _(expr, assumptions):
    return _PrimePredicate_number(expr, assumptions)


def _(expr, assumptions):
    return None


def _(expr, assumptions):
    ret = expr.is_composite
    if ret is None:
        raise MDNotImplementedError
    return ret


def _(expr, assumptions):
    _positive = ask(Q.positive(expr), assumptions)
    if _positive:
        _integer = ask(Q.integer(expr), assumptions)
        if _integer:
            _prime = ask(Q.prime(expr), assumptions)
            if _prime is None:
                return
            # Positive integer which is not prime is not
            # necessarily composite
            _is_one = ask(Q.eq(expr, 1), assumptions)
            if _is_one:
                return False
            if _is_one is None:
                return None
            return not _prime
        else:
            return _integer
    else:
        return _positive


def _(expr, assumptions):
    ret = expr.is_even
    if ret is None:
        raise MDNotImplementedError
    return ret


def _(expr, assumptions):
    if expr.is_number:
        return _EvenPredicate_number(expr, assumptions)


def _(expr, assumptions):
    """
    Even * Integer    -> Even
    Even * Odd        -> Even
    Integer * Odd     -> ?
    Odd * Odd         -> Odd
    Even * Even       -> Even
    Integer * Integer -> Even if Integer + Integer = Odd
    otherwise         -> ?
    """
    if expr.is_number:
        return _EvenPredicate_number(expr, assumptions)
    even, odd, irrational, acc = False, 0, False, 1
    for arg in expr.args:
        # check for all integers and at least one even
        if ask(Q.integer(arg), assumptions):
            if ask(Q.even(arg), assumptions):
                even = True
            elif ask(Q.odd(arg), assumptions):
                odd += 1
            elif not even and acc != 1:
                if ask(Q.odd(acc + arg), assumptions):
                    even = True
        elif ask(Q.irrational(arg), assumptions):
            # one irrational makes the result False
            # two makes it undefined
            if irrational:
                break
            irrational = True
        else:
            break
        acc = arg
    else:
        if irrational:
            return False
        if even:
            return True
        if odd == len(expr.args):
            return False


def _(expr, assumptions):
    """
    Even + Odd  -> Odd
    Even + Even -> Even
    Odd  + Odd  -> Even

    """
    if expr.is_number:
        return _EvenPredicate_number(expr, assumptions)
    _result = True
    for arg in expr.args:
        if ask(Q.even(arg), assumptions):
            pass
        elif ask(Q.odd(arg), assumptions):
            _result = not _result
        else:
            break
    else:
        return _result


def _(expr, assumptions):
    if expr.is_number:
        return _EvenPredicate_number(expr, assumptions)
    if ask(Q.integer(expr.exp), assumptions):
        if ask(Q.positive(expr.exp), assumptions):
            return ask(Q.even(expr.base), assumptions)
        elif ask(~Q.negative(expr.exp) & Q.odd(expr.base), assumptions):
            return False
        elif expr.base is S.NegativeOne:
            return False


def _(expr, assumptions):
    return not bool(expr.p & 1)


def _(expr, assumptions):
    return False


def _(expr, assumptions):
    return _EvenPredicate_number(expr, assumptions)


def _(expr, assumptions):
    if ask(Q.real(expr.args[0]), assumptions):
        return ask(Q.even(expr.args[0]), assumptions)


def _(expr, assumptions):
    if ask(Q.real(expr.args[0]), assumptions):
        return ask(Q.even(expr.args[0]), assumptions)


def _(expr, assumptions):
    if ask(Q.real(expr.args[0]), assumptions):
        return True


def _(expr, assumptions):
    return None


def _(expr, assumptions):
    ret = expr.is_odd
    if ret is None:
        raise MDNotImplementedError
    return ret


def _(expr, assumptions):
    _integer = ask(Q.integer(expr), assumptions)
    if _integer:
        _even = ask(Q.even(expr), assumptions)
        if _even is None:
            return None
        return not _even
    return _integer


def _(expr, assumptions):
    if expr.is_number:
        return _NegativePredicate_number(expr, assumptions)


def _(expr, assumptions):
    ret = expr.is_negative
    if ret is None:
        raise MDNotImplementedError
    return ret


def _(expr, assumptions):
    """
    Positive + Positive -> Positive,
    Negative + Negative -> Negative
    """
    if expr.is_number:
        return _NegativePredicate_number(expr, assumptions)

    r = ask(Q.real(expr), assumptions)
    if r is not True:
        return r

    nonpos = 0
    for arg in expr.args:
        if ask(Q.negative(arg), assumptions) is not True:
            if ask(Q.positive(arg), assumptions) is False:
                nonpos += 1
            else:
                break
    else:
        if nonpos < len(expr.args):
            return True


def _(expr, assumptions):
    if expr.is_number:
        return _NegativePredicate_number(expr, assumptions)
    result = None
    for arg in expr.args:
        if result is None:
            result = False
        if ask(Q.negative(arg), assumptions):
            result = not result
        elif ask(Q.positive(arg), assumptions):
            pass
        else:
            return
    return result


def _(expr, assumptions):
    """
    Real ** Even -> NonNegative
    Real ** Odd  -> same_as_base
    NonNegative ** Positive -> NonNegative
    """
    if expr.base == E:
        # Exponential is always positive:
        if ask(Q.real(expr.exp), assumptions):
            return False
        return

    if expr.is_number:
        return _NegativePredicate_number(expr, assumptions)
    if ask(Q.real(expr.base), assumptions):
        if ask(Q.positive(expr.base), assumptions):
            if ask(Q.real(expr.exp), assumptions):
                return False
        if ask(Q.even(expr.exp), assumptions):
            return False
        if ask(Q.odd(expr.exp), assumptions):
            return ask(Q.negative(expr.base), assumptions)


def _(expr, assumptions):
    return False


def _(expr, assumptions):
    if ask(Q.real(expr.exp), assumptions):
        return False
    raise MDNotImplementedError


def _(expr, assumptions):
    if expr.is_number:
        notnegative = fuzzy_not(_NegativePredicate_number(expr, assumptions))
        if notnegative:
            return ask(Q.real(expr), assumptions)
        else:
            return notnegative


def _(expr, assumptions):
    ret = expr.is_nonnegative
    if ret is None:
        raise MDNotImplementedError
    return ret


def _(expr, assumptions):
    ret = expr.is_nonzero
    if ret is None:
        raise MDNotImplementedError
    return ret


def _(expr, assumptions):
    if ask(Q.real(expr)) is False:
        return False
    if expr.is_number:
        # if there are no symbols just evalf
        i = expr.evalf(2)
        def nonz(i):
            if i._prec != 1:
                return i != 0
        return fuzzy_or(nonz(i) for i in i.as_real_imag())


def _(expr, assumptions):
    if all(ask(Q.positive(x), assumptions) for x in expr.args) \
            or all(ask(Q.negative(x), assumptions) for x in expr.args):
        return True


def _(expr, assumptions):
    for arg in expr.args:
        result = ask(Q.nonzero(arg), assumptions)
        if result:
            continue
        return result
    return True


def _(expr, assumptions):
    return ask(Q.nonzero(expr.base), assumptions)


def _(expr, assumptions):
    return ask(Q.nonzero(expr.args[0]), assumptions)


def _(expr, assumptions):
    return None


def _(expr, assumptions):
    ret = expr.is_zero
    if ret is None:
        raise MDNotImplementedError
    return ret


def _(expr, assumptions):
    return fuzzy_and([fuzzy_not(ask(Q.nonzero(expr), assumptions)),
        ask(Q.real(expr), assumptions)])


def _(expr, assumptions):
    # TODO: This should be deducible from the nonzero handler
    return fuzzy_or(ask(Q.zero(arg), assumptions) for arg in expr.args)


def _(expr, assumptions):
    ret = expr.is_nonpositive
    if ret is None:
        raise MDNotImplementedError
    return ret


def _(expr, assumptions):
    if expr.is_number:
        notpositive = fuzzy_not(_PositivePredicate_number(expr, assumptions))
        if notpositive:
            return ask(Q.real(expr), assumptions)
        else:
            return notpositive


def _(expr, assumptions):
    ret = expr.is_positive
    if ret is None:
        raise MDNotImplementedError
    return ret


def _(expr, assumptions):
    if expr.is_number:
        return _PositivePredicate_number(expr, assumptions)


def _(expr, assumptions):
    if expr.is_number:
        return _PositivePredicate_number(expr, assumptions)
    result = True
    for arg in expr.args:
        if ask(Q.positive(arg), assumptions):
            continue
        elif ask(Q.negative(arg), assumptions):
            result = result ^ True
        else:
            return
    return result


def _(expr, assumptions):
    if expr.is_number:
        return _PositivePredicate_number(expr, assumptions)

    r = ask(Q.real(expr), assumptions)
    if r is not True:
        return r

    nonneg = 0
    for arg in expr.args:
        if ask(Q.positive(arg), assumptions) is not True:
            if ask(Q.negative(arg), assumptions) is False:
                nonneg += 1
            else:
                break
    else:
        if nonneg < len(expr.args):
            return True


def _(expr, assumptions):
    if expr.base == E:
        if ask(Q.real(expr.exp), assumptions):
            return True
        if ask(Q.imaginary(expr.exp), assumptions):
            return ask(Q.even(expr.exp/(I*pi)), assumptions)
        return

    if expr.is_number:
        return _PositivePredicate_number(expr, assumptions)
    if ask(Q.positive(expr.base), assumptions):
        if ask(Q.real(expr.exp), assumptions):
            return True
    if ask(Q.negative(expr.base), assumptions):
        if ask(Q.even(expr.exp), assumptions):
            return True
        if ask(Q.odd(expr.exp), assumptions):
            return False


def _(expr, assumptions):
    if ask(Q.real(expr.exp), assumptions):
        return True
    if ask(Q.imaginary(expr.exp), assumptions):
        return ask(Q.even(expr.exp/(I*pi)), assumptions)


def _(expr, assumptions):
    r = ask(Q.real(expr.args[0]), assumptions)
    if r is not True:
        return r
    if ask(Q.positive(expr.args[0] - 1), assumptions):
        return True
    if ask(Q.negative(expr.args[0] - 1), assumptions):
        return False


def _(expr, assumptions):
    x = expr.args[0]
    if ask(Q.integer(x) & Q.positive(x), assumptions):
            return True


def _(expr, assumptions):
    return False


def _(expr, assumptions):
    return ask(Q.nonzero(expr), assumptions)


def _(expr, assumptions):
    if ask(Q.positive_definite(expr.arg), assumptions):
        return True


def _(expr, assumptions):
    if ask(Q.positive_definite(expr.arg), assumptions):
        return True


def _(expr, assumptions):
    if (expr.i == expr.j
            and ask(Q.positive_definite(expr.parent), assumptions)):
        return True


def _(expr, assumptions):
    return ask(Q.positive(expr.args[0]), assumptions)


def _(expr, assumptions):
    x = expr.args[0]
    if ask(Q.positive(x) & Q.nonpositive(x - 1), assumptions):
        return True
    if ask(Q.negative(x) & Q.nonnegative(x + 1), assumptions):
        return False


def _(expr, assumptions):
    x = expr.args[0]
    if ask(Q.nonpositive(x - 1) & Q.nonnegative(x + 1), assumptions):
        return True


def _(expr, assumptions):
    return ask(Q.real(expr.args[0]), assumptions)


def _(expr, assumptions):
    return None


def _(expr, assumptions):
    return ask(Q.negative(expr) | Q.negative_infinite(expr), assumptions)


def _(expr, assumptions):
    return ask(Q.positive(expr) | Q.positive_infinite(expr), assumptions)


def _(expr, assumptions):
    return ask(
        Q.negative_infinite(expr) | Q.negative(expr) | Q.positive(expr) | Q.positive_infinite(expr),
        assumptions)


def _(expr, assumptions):
    return ask(
        Q.negative_infinite(expr) | Q.negative(expr) | Q.zero(expr),
        assumptions)


def _(expr, assumptions):
    return ask(
        Q.zero(expr) | Q.positive(expr) | Q.positive_infinite(expr),
        assumptions)


def _(expr, assumptions):
    return True


def _(expr, assumptions):
    return False


def _(expr, assumptions):
    ret = expr.is_integer
    if ret is None:
        raise MDNotImplementedError
    return ret


def _(expr, assumptions):
    """
    * Integer + Integer       -> Integer
    * Integer + !Integer      -> !Integer
    * !Integer + !Integer -> ?
    """
    if expr.is_number:
        return _IntegerPredicate_number(expr, assumptions)
    return test_closed_group(expr, assumptions, Q.integer)


def _(expr,assumptions):
    if expr.is_number:
        return _IntegerPredicate_number(expr, assumptions)
    if ask_all(~Q.zero(expr.base), Q.finite(expr.base), Q.zero(expr.exp), assumptions=assumptions):
        return True
    if ask_all(Q.integer(expr.base), Q.integer(expr.exp), assumptions=assumptions):
        if ask_any(Q.positive(expr.exp), Q.nonnegative(expr.exp) & ~Q.zero(expr.base), Q.zero(expr.base-1), Q.zero(expr.base+1), assumptions=assumptions):
            return True


def _(expr, assumptions):
    """
    * Integer*Integer      -> Integer
    * Integer*Irrational   -> !Integer
    * Odd/Even             -> !Integer
    * Integer*Rational     -> ?
    """
    if expr.is_number:
        return _IntegerPredicate_number(expr, assumptions)
    _output = True
    for arg in expr.args:
        if not ask(Q.integer(arg), assumptions):
            if arg.is_Rational:
                if arg.q == 2:
                    return ask(Q.even(2*expr), assumptions)
                if ~(arg.q & 1):
                    return None
            elif ask(Q.irrational(arg), assumptions):
                if _output:
                    _output = False
                else:
                    return
            else:
                return

    return _output


def _(expr, assumptions):
    if ask(Q.integer(expr.args[0]), assumptions):
        return True


def _(expr, assumptions):
    return ask(Q.integer_elements(expr.args[0]), assumptions)


def _(expr, assumptions):
    return True


def _(expr, assumptions):
    return None


def _(expr, assumptions):
    return False


def _(expr, assumptions):
    ret = expr.is_rational
    if ret is None:
        raise MDNotImplementedError
    return ret


def _(expr, assumptions):
    """
    * Rational + Rational     -> Rational
    * Rational + !Rational    -> !Rational
    * !Rational + !Rational   -> ?
    """
    if expr.is_number:
        if expr.as_real_imag()[1]:
            return False
    return test_closed_group(expr, assumptions, Q.rational)


def _(expr, assumptions):
    """
    * Rational ** Integer      -> Rational
    * Irrational ** Rational   -> Irrational
    * Rational ** Irrational   -> ?
    """
    if expr.base == E:
        x = expr.exp
        if ask(Q.rational(x), assumptions):
            return ask(Q.zero(x), assumptions)
        return

    is_exp_integer = ask(Q.integer(expr.exp), assumptions)
    if is_exp_integer:
        is_base_rational = ask(Q.rational(expr.base),assumptions)
        if is_base_rational:
            is_base_zero = ask(Q.zero(expr.base),assumptions)
            if is_base_zero is False:
                return True
            if is_base_zero and ask(Q.positive(expr.exp)):
                return True
        if ask(Q.algebraic(expr.base),assumptions) is False:
            return ask(Q.zero(expr.exp), assumptions)
        if ask(Q.irrational(expr.base),assumptions) and ask(Q.eq(expr.exp,-1)):
            return False
        return
    elif ask(Q.rational(expr.exp), assumptions):
        if ask(Q.prime(expr.base), assumptions) and is_exp_integer is False:
            return False
        if ask(Q.zero(expr.base)) and ask(Q.positive(expr.exp)):
            return True
        if ask(Q.eq(expr.base,1)):
            return True


def _(expr, assumptions):
    x = expr.args[0]
    if ask(Q.rational(x), assumptions):
        return ask(~Q.nonzero(x), assumptions)


def _(expr, assumptions):
    x = expr.exp
    if ask(Q.rational(x), assumptions):
        return ask(~Q.nonzero(x), assumptions)


def _(expr, assumptions):
    x = expr.args[0]
    if ask(Q.rational(x), assumptions):
        return False


def _(expr, assumptions):
    x = expr.args[0]
    if ask(Q.rational(x), assumptions):
        return ask(~Q.nonzero(x - 1), assumptions)


def _(expr, assumptions):
    ret = expr.is_irrational
    if ret is None:
        raise MDNotImplementedError
    return ret


def _(expr, assumptions):
    _real = ask(Q.real(expr), assumptions)
    if _real:
        _rational = ask(Q.rational(expr), assumptions)
        if _rational is None:
            return None
        return not _rational
    else:
        return _real


def _(expr, assumptions):
    return True


def _(expr, assumptions):
    return False


def _(expr, assumptions):
    ret = expr.is_real
    if ret is None:
        raise MDNotImplementedError
    return ret


def _(expr, assumptions):
    """
    * Real + Real              -> Real
    * Real + (Complex & !Real) -> !Real
    """
    if expr.is_number:
        return _RealPredicate_number(expr, assumptions)
    return test_closed_group(expr, assumptions, Q.real)


def _(expr, assumptions):
    """
    * Real*Real               -> Real
    * Real*Imaginary          -> !Real
    * Imaginary*Imaginary     -> Real
    """
    if expr.is_number:
        return _RealPredicate_number(expr, assumptions)
    result = True
    for arg in expr.args:
        if ask(Q.real(arg), assumptions):
            pass
        elif ask(Q.imaginary(arg), assumptions):
            result = result ^ True
        else:
            break
    else:
        return result


def _(expr, assumptions):
    """
    * Real**Integer              -> Real
    * Positive**Real             -> Real
    * Negative**Real             -> ?
    * Real**(Integer/Even)       -> Real if base is nonnegative
    * Real**(Integer/Odd)        -> Real
    * Imaginary**(Integer/Even)  -> Real
    * Imaginary**(Integer/Odd)   -> not Real
    * Imaginary**Real            -> ? since Real could be 0 (giving real)
                                    or 1 (giving imaginary)
    * b**Imaginary               -> Real if log(b) is imaginary and b != 0
                                    and exponent != integer multiple of
                                    I*pi/log(b)
    * Real**Real                 -> ? e.g. sqrt(-1) is imaginary and
                                    sqrt(2) is not
    """
    if expr.is_number:
        return _RealPredicate_number(expr, assumptions)

    if expr.base == E:
        return ask(
            Q.integer(expr.exp/I/pi) | Q.real(expr.exp), assumptions
        )

    if expr.base.func == exp or (expr.base.is_Pow and expr.base.base == E):
        if ask(Q.imaginary(expr.base.exp), assumptions):
            if ask(Q.imaginary(expr.exp), assumptions):
                return True
        # If the i = (exp's arg)/(I*pi) is an integer or half-integer
        # multiple of I*pi then 2*i will be an integer. In addition,
        # exp(i*I*pi) = (-1)**i so the overall realness of the expr
        # can be determined by replacing exp(i*I*pi) with (-1)**i.
        i = expr.base.exp/I/pi
        if ask(Q.integer(2*i), assumptions):
            return ask(Q.real((S.NegativeOne**i)**expr.exp), assumptions)
        return

    if ask(Q.imaginary(expr.base), assumptions):
        if ask(Q.integer(expr.exp), assumptions):
            odd = ask(Q.odd(expr.exp), assumptions)
            if odd is not None:
                return not odd
            return

    if ask(Q.imaginary(expr.exp), assumptions):
        imlog = ask(Q.imaginary(log(expr.base)), assumptions)
        if imlog is not None:
            # I**i -> real, log(I) is imag;
            # (2*I)**i -> complex, log(2*I) is not imag
            return imlog

    if ask(Q.real(expr.base), assumptions):
        if ask(Q.real(expr.exp), assumptions):
            if ask(Q.zero(expr.base), assumptions) is not False:
                if ask(Q.positive(expr.exp), assumptions):
                    return True
                return
            if expr.exp.is_Rational and \
                    ask(Q.even(expr.exp.q), assumptions):
                return ask(Q.positive(expr.base), assumptions)
            elif ask(Q.integer(expr.exp), assumptions):
                return True
            elif ask(Q.positive(expr.base), assumptions):
                return True


def _(expr, assumptions):
    if ask(Q.real(expr.args[0]), assumptions):
            return True


def _(expr, assumptions):
    return ask(
        Q.integer(expr.exp/I/pi) | Q.real(expr.exp), assumptions
    )


def _(expr, assumptions):
    return ask(Q.positive(expr.args[0]), assumptions)


def _(expr, assumptions):
    return ask(Q.real_elements(expr.args[0]), assumptions)


def _(expr, assumptions):
    return ask(Q.negative_infinite(expr)
               | Q.negative(expr)
               | Q.zero(expr)
               | Q.positive(expr)
               | Q.positive_infinite(expr),
            assumptions)


def _(expr, assumptions):
    return True


def _(expr, assumptions):
    return test_closed_group(expr, assumptions, Q.extended_real)


def _(expr, assumptions):
    if isinstance(expr, MatrixBase):
        return None
    return ask(Q.real(expr), assumptions)


def _(expr, assumptions):
    """
    * Hermitian + Hermitian  -> Hermitian
    * Hermitian + !Hermitian -> !Hermitian
    """
    if expr.is_number:
        raise MDNotImplementedError
    return test_closed_group(expr, assumptions, Q.hermitian)


def _(expr, assumptions):
    """
    As long as there is at most only one noncommutative term:

    * Hermitian*Hermitian         -> Hermitian
    * Hermitian*Antihermitian     -> !Hermitian
    * Antihermitian*Antihermitian -> Hermitian
    """
    if expr.is_number:
        raise MDNotImplementedError
    nccount = 0
    result = True
    for arg in expr.args:
        if ask(Q.antihermitian(arg), assumptions):
            result = result ^ True
        elif not ask(Q.hermitian(arg), assumptions):
            break
        if ask(~Q.commutative(arg), assumptions):
            nccount += 1
            if nccount > 1:
                break
    else:
        return result


def _(expr, assumptions):
    """
    * Hermitian**Integer -> Hermitian
    """
    if expr.is_number:
        raise MDNotImplementedError
    if expr.base == E:
        if ask(Q.hermitian(expr.exp), assumptions):
            return True
        raise MDNotImplementedError
    if ask(Q.hermitian(expr.base), assumptions):
        if ask(Q.integer(expr.exp), assumptions):
            return True
    raise MDNotImplementedError


def _(expr, assumptions):
    if ask(Q.hermitian(expr.args[0]), assumptions):
        return True
    raise MDNotImplementedError


def _(expr, assumptions):
    if ask(Q.hermitian(expr.exp), assumptions):
        return True
    raise MDNotImplementedError


def _(mat, assumptions):
    rows, cols = mat.shape
    ret_val = True
    for i in range(rows):
        for j in range(i, cols):
            cond = fuzzy_bool(Eq(mat[i, j], conjugate(mat[j, i])))
            if cond is None:
                ret_val = None
            if cond == False:
                return False
    if ret_val is None:
        raise MDNotImplementedError
    return ret_val


def _(expr, assumptions):
    return True


def _(expr, assumptions):
    return False


def _(expr, assumptions):
    ret = expr.is_complex
    if ret is None:
        raise MDNotImplementedError
    return ret


def _(expr, assumptions):
    return test_closed_group(expr, assumptions, Q.complex)


def _(expr, assumptions):
    if expr.base == E:
        return True
    return test_closed_group(expr, assumptions, Q.complex)


def _(expr, assumptions):
    return ask(Q.complex_elements(expr.args[0]), assumptions)


def _(expr, assumptions):
    return None


def _(expr, assumptions):
    return True


def _(expr, assumptions):
    ret = expr.is_imaginary
    if ret is None:
        raise MDNotImplementedError
    return ret


def _(expr, assumptions):
    """
    * Imaginary + Imaginary -> Imaginary
    * Imaginary + Complex   -> ?
    * Imaginary + Real      -> !Imaginary
    """
    if expr.is_number:
        return _Imaginary_number(expr, assumptions)

    reals = 0
    for arg in expr.args:
        if ask(Q.imaginary(arg), assumptions):
            pass
        elif ask(Q.real(arg), assumptions):
            reals += 1
        else:
            break
    else:
        if reals == 0:
            return True
        if reals in (1, len(expr.args)):
            # two reals could sum 0 thus giving an imaginary
            return False


def _(expr, assumptions):
    """
    * Real*Imaginary      -> Imaginary
    * Imaginary*Imaginary -> Real
    """
    if expr.is_number:
        return _Imaginary_number(expr, assumptions)
    result = False
    reals = 0
    for arg in expr.args:
        if ask(Q.imaginary(arg), assumptions):
            result = result ^ True
        elif not ask(Q.real(arg), assumptions):
            break
    else:
        if reals == len(expr.args):
            return False
        return result


def _(expr, assumptions):
    """
    * Imaginary**Odd        -> Imaginary
    * Imaginary**Even       -> Real
    * b**Imaginary          -> !Imaginary if exponent is an integer
                               multiple of I*pi/log(b)
    * Imaginary**Real       -> ?
    * Positive**Real        -> Real
    * Negative**Integer     -> Real
    * Negative**(Integer/2) -> Imaginary
    * Negative**Real        -> not Imaginary if exponent is not Rational
    """
    if expr.is_number:
        return _Imaginary_number(expr, assumptions)

    if expr.base == E:
        a = expr.exp/I/pi
        return ask(Q.integer(2*a) & ~Q.integer(a), assumptions)

    if expr.base.func == exp or (expr.base.is_Pow and expr.base.base == E):
        if ask(Q.imaginary(expr.base.exp), assumptions):
            if ask(Q.imaginary(expr.exp), assumptions):
                return False
            i = expr.base.exp/I/pi
            if ask(Q.integer(2*i), assumptions):
                return ask(Q.imaginary((S.NegativeOne**i)**expr.exp), assumptions)

    if ask(Q.imaginary(expr.base), assumptions):
        if ask(Q.integer(expr.exp), assumptions):
            odd = ask(Q.odd(expr.exp), assumptions)
            if odd is not None:
                return odd
            return

    if ask(Q.imaginary(expr.exp), assumptions):
        imlog = ask(Q.imaginary(log(expr.base)), assumptions)
        if imlog is not None:
            # I**i -> real; (2*I)**i -> complex ==> not imaginary
            return False

    if ask(Q.real(expr.base) & Q.real(expr.exp), assumptions):
        if ask(Q.positive(expr.base), assumptions):
            return False
        else:
            rat = ask(Q.rational(expr.exp), assumptions)
            if not rat:
                return rat
            if ask(Q.integer(expr.exp), assumptions):
                return False
            else:
                half = ask(Q.integer(2*expr.exp), assumptions)
                if half:
                    return ask(Q.negative(expr.base), assumptions)
                return half


def _(expr, assumptions):
    if ask(Q.real(expr.args[0]), assumptions):
        if ask(Q.positive(expr.args[0]), assumptions):
            return False
        return
    # XXX it should be enough to do
    # return ask(Q.nonpositive(expr.args[0]), assumptions)
    # but ask(Q.nonpositive(exp(x)), Q.imaginary(x)) -> None;
    # it should return True since exp(x) will be either 0 or complex
    if expr.args[0].func == exp or (expr.args[0].is_Pow and expr.args[0].base == E):
        if expr.args[0].exp in [I, -I]:
            return True
    im = ask(Q.imaginary(expr.args[0]), assumptions)
    if im is False:
        return False


def _(expr, assumptions):
    a = expr.exp/I/pi
    return ask(Q.integer(2*a) & ~Q.integer(a), assumptions)


def _(expr, assumptions):
    return not (expr.as_real_imag()[1] == 0)


def _(expr, assumptions):
    return None


def _(expr, assumptions):
    if isinstance(expr, MatrixBase):
        return None
    if ask(Q.zero(expr), assumptions):
        return True
    return ask(Q.imaginary(expr), assumptions)


def _(expr, assumptions):
    """
    * Antihermitian + Antihermitian  -> Antihermitian
    * Antihermitian + !Antihermitian -> !Antihermitian
    """
    if expr.is_number:
        raise MDNotImplementedError
    return test_closed_group(expr, assumptions, Q.antihermitian)


def _(expr, assumptions):
    """
    As long as there is at most only one noncommutative term:

    * Hermitian*Hermitian         -> !Antihermitian
    * Hermitian*Antihermitian     -> Antihermitian
    * Antihermitian*Antihermitian -> !Antihermitian
    """
    if expr.is_number:
        raise MDNotImplementedError
    nccount = 0
    result = False
    for arg in expr.args:
        if ask(Q.antihermitian(arg), assumptions):
            result = result ^ True
        elif not ask(Q.hermitian(arg), assumptions):
            break
        if ask(~Q.commutative(arg), assumptions):
            nccount += 1
            if nccount > 1:
                break
    else:
        return result


def _(expr, assumptions):
    """
    * Hermitian**Integer  -> !Antihermitian
    * Antihermitian**Even -> !Antihermitian
    * Antihermitian**Odd  -> Antihermitian
    """
    if expr.is_number:
        raise MDNotImplementedError
    if ask(Q.hermitian(expr.base), assumptions):
        if ask(Q.integer(expr.exp), assumptions):
            return False
    elif ask(Q.antihermitian(expr.base), assumptions):
        if ask(Q.even(expr.exp), assumptions):
            return False
        elif ask(Q.odd(expr.exp), assumptions):
            return True
    raise MDNotImplementedError


def _(mat, assumptions):
    rows, cols = mat.shape
    ret_val = True
    for i in range(rows):
        for j in range(i, cols):
            cond = fuzzy_bool(Eq(mat[i, j], -conjugate(mat[j, i])))
            if cond is None:
                ret_val = None
            if cond == False:
                return False
    if ret_val is None:
        raise MDNotImplementedError
    return ret_val


def _(expr, assumptions):
    return True


def _(expr, assumptions):
    return False


def _(expr, assumptions):
    return test_closed_group(expr, assumptions, Q.algebraic)


def _(expr, assumptions):
    if expr.base == E:
        if ask(Q.algebraic(expr.exp), assumptions):
            return ask(~Q.nonzero(expr.exp), assumptions)
        return
    if expr.base == pi:
        if ask(Q.integer(expr.exp), assumptions) and ask(Q.positive(expr.exp), assumptions):
            return False
        return
    exp_rational = ask(Q.rational(expr.exp), assumptions)
    base_algebraic = ask(Q.algebraic(expr.base), assumptions)
    exp_algebraic = ask(Q.algebraic(expr.exp),assumptions)
    if base_algebraic and exp_algebraic:
        if exp_rational:
            return True
        # Check based on the Gelfond-Schneider theorem:
        # If the base is algebraic and not equal to 0 or 1, and the exponent
        # is irrational,then the result is transcendental.
        if ask(Q.ne(expr.base,0) & Q.ne(expr.base,1)) and exp_rational is False:
            return False


def _(expr, assumptions):
    return expr.q != 0


def _(expr, assumptions):
    x = expr.args[0]
    if ask(Q.algebraic(x), assumptions):
        return ask(~Q.nonzero(x), assumptions)


def _(expr, assumptions):
    x = expr.exp
    if ask(Q.algebraic(x), assumptions):
        return ask(~Q.nonzero(x), assumptions)


def _(expr, assumptions):
    x = expr.args[0]
    if ask(Q.algebraic(x), assumptions):
        return False


def _(expr, assumptions):
    x = expr.args[0]
    if ask(Q.algebraic(x), assumptions):
        return ask(~Q.nonzero(x - 1), assumptions)


def _(name: str, *args, **kwargs):
    return mkpath(pathlib.Path(name), *args, **kwargs)


def _(name: None, *args, **kwargs):
    """
    Detect a common bug -- name is None.
    """
    raise DistutilsInternalError(f"mkpath: 'name' must be a string (got {name!r})")


def _(text: str) -> Iterator[str]:
    return filter(_nonblank, map(str.strip, text.splitlines()))


def _(args: collections.abc.Mapping, func):
    """Splat kargs to func as kwargs."""
    return func(**args)


def _(text):
    return clean(text.splitlines())


def _(diff_n):
    diff_n = _nonneg_int_or_fail(diff_n, "diff_n", strict=False)
    if not 0 <= diff_n <= 2:
        raise ValueError(
            "diff_n is currently only implemented for orders 0, 1, and 2,"
            f" received: {diff_n}."
        )
    return diff_n


def _(out):
    return np.moveaxis(out, -1, 0)


def _(diff_n):
    diff_n = _nonneg_int_or_fail(diff_n, "diff_n", strict=False)
    if not 0 <= diff_n <= 2:
        raise ValueError(
            "diff_n is currently only implemented for orders 0, 1, and 2,"
            f" received: {diff_n}."
        )
    return diff_n


def _(diff_n):
    return {'axes': [()] + [(0, 1, -1)]}


def _(n, m, theta_shape, nout, diff_n):
    if not isinstance(n, numbers.Integral) or (n < 0):
        raise ValueError("n must be a non-negative integer.")

    return ((n + 1, 2 * abs(m) + 1) + theta_shape + (diff_n + 1,),)


def _(out):
    return np.moveaxis(out, -1, 0)


def _(branch_cut, norm, diff_n):
    diff_n = _nonneg_int_or_fail(diff_n, "diff_n", strict=False)
    if not 0 <= diff_n <= 2:
        raise ValueError(
            "diff_n is currently only implemented for orders 0, 1, and 2,"
            f" received: {diff_n}."
        )
    return norm, diff_n


def _(branch_cut, norm, diff_n):
    return branch_cut,


def _(out):
    return np.moveaxis(out, -1, 0)


def _(branch_cut, norm, diff_n):
    if not ((isinstance(diff_n, numbers.Integral))
            and diff_n >= 0):
        raise ValueError(
            f"diff_n must be a non-negative integer, received: {diff_n}."
        )
    if not 0 <= diff_n <= 2:
        raise ValueError(
            "diff_n is currently only implemented for orders 0, 1, and 2,"
            f" received: {diff_n}."
        )
    return norm, diff_n


def _(branch_cut, norm, diff_n):
    return branch_cut,


def _(branch_cut, norm, diff_n):
    return {'axes': [(), ()] + [(0, 1, -1)]}


def _(n, m, z_shape, branch_cut_shape, nout, **kwargs):
    diff_n = kwargs['diff_n']

    if not isinstance(n, numbers.Integral) or (n < 0):
        raise ValueError("n must be a non-negative integer.")
    if not isinstance(m, numbers.Integral) or (m < 0):
        raise ValueError("m must be a non-negative integer.")

    return ((n + 1, 2 * abs(m) + 1) +
        np.broadcast_shapes(z_shape, branch_cut_shape) + (diff_n + 1,),)


def _(out):
    return np.moveaxis(out, -1, 0)


def _(diff_n):
    if (not isinstance(diff_n, numbers.Integral)) or (diff_n < 0):
        raise ValueError(
            f"diff_n must be a non-negative integer, received: {diff_n}."
        )
    if not 0 <= diff_n <= 2:
        raise NotImplementedError(
            "diff_n is currently only implemented for orders 0, 1, and 2,"
            f" received: {diff_n}."
        )
    return diff_n


def _(out):
    return np.moveaxis(out, -1, 0)


def _(diff_n):
    diff_n = _nonneg_int_or_fail(diff_n, "diff_n", strict=False)
    if not 0 <= diff_n <= 2:
        raise ValueError(
            "diff_n is currently only implemented for orders 0, 1, and 2,"
            f" received: {diff_n}."
        )
    return diff_n


def _(diff_n):
    return {'axes': [(), (0, -1)]}


def _(n, z_shape, nout, diff_n):
    n = _nonneg_int_or_fail(n, 'n', strict=False)

    return nout * ((n + 1,) + z_shape + (diff_n + 1,),)


def _(out):
    return np.moveaxis(out, -1, 0)


def _(diff_n):
    diff_n = _nonneg_int_or_fail(diff_n, "diff_n", strict=False)
    if not 0 <= diff_n <= 2:
        raise ValueError(
            "diff_n is currently only implemented for orders 0, 1, and 2,"
            f" received: {diff_n}."
        )
    return diff_n


def _(out):
    if (out.shape[-1] == 1):
        return out[..., 0, 0]

    if (out.shape[-1] == 2):
        return out[..., 0, 0], out[..., [1, 0], [0, 1]]

    if (out.shape[-1] == 3):
        return (out[..., 0, 0], out[..., [1, 0], [0, 1]],
            out[..., [[2, 1], [1, 0]], [[0, 1], [1, 2]]])


def _(diff_n):
    diff_n = _nonneg_int_or_fail(diff_n, "diff_n", strict=False)
    if not 0 <= diff_n <= 2:
        raise ValueError(
            "diff_n is currently only implemented for orders 2,"
            f" received: {diff_n}."
        )
    return diff_n


def _(diff_n):
    return {'axes': [(), ()] + [(0, 1, -2, -1)]}


def _(n, m, theta_shape, phi_shape, nout, **kwargs):
    diff_n = kwargs['diff_n']

    if not isinstance(n, numbers.Integral) or (n < 0):
        raise ValueError("n must be a non-negative integer.")

    return ((n + 1, 2 * abs(m) + 1) + np.broadcast_shapes(theta_shape, phi_shape) +
        (diff_n + 1, diff_n + 1),)


def _(out):
    if (out.shape[-1] == 1):
        return out[..., 0, 0]

    if (out.shape[-1] == 2):
        return out[..., 0, 0], out[..., [1, 0], [0, 1]]

    if (out.shape[-1] == 3):
        return (out[..., 0, 0], out[..., [1, 0], [0, 1]],
            out[..., [[2, 1], [1, 0]], [[0, 1], [1, 2]]])


def _(node: nodes.ClassDef | bases.Instance) -> Iterable[str]:
    values = itertools.chain(node.instance_attrs.keys(), node.locals.keys())

    try:
        mro = node.mro()[1:]
    except (NotImplementedError, TypeError, astroid.MroError):
        mro = node.ancestors()

    other_values = [value for cls in mro for value in _node_names(cls)]
    return itertools.chain(values, other_values)


def _(text):
    return filter(_nonblank, map(str.strip, text.splitlines()))


def _(*consts_and_args, jaxpr, num_consts, **_):
  consts, args = util.split_list(consts_and_args, [num_consts])
  return jax_core.eval_jaxpr(jaxpr, consts, *args)


def _(*args, jaxpr, **kwargs):
  del args, kwargs
  return [v.aval for v in jaxpr.outvars], jaxpr.effects


def _(base_io_obj, file, *, loop=None, executor=None):
    return AsyncTextIOWrapper(file, loop=loop, executor=executor)


def _(base_io_obj, file, *, loop=None, executor=None):
    return AsyncBufferedIOBase(file, loop=loop, executor=executor)


def _(base_io_obj, file, *, loop=None, executor=None):
    return AsyncBufferedReader(file, loop=loop, executor=executor)


def _(base_io_obj, file, *, loop=None, executor=None):
    return AsyncFileIO(file, loop=loop, executor=executor)


def _(file, *, loop=None, executor=None):
    return AsyncTextIOWrapper(file, loop=loop, executor=executor)


def _(file, *, loop=None, executor=None):
    return AsyncBufferedIOBase(file, loop=loop, executor=executor)


def _(file, *, loop=None, executor=None):
    return AsyncBufferedReader(file, loop=loop, executor=executor)


def _(file, *, loop=None, executor=None):
    return AsyncFileIO(file, loop=loop, executor=executor)

