
def register_decomposition(
    aten_op: torch._ops.OpOverload,
    registry: dict[str, torch.jit.ScriptFunction] | None = None,
) -> Callable[[Callable[_P, _T]], Callable[_P, _T]]:
    def decomposition_decorator(f: Callable[_P, _T]) -> Callable[_P, _T]:
        nonlocal registry
        if registry is None:
            registry = decomposition_table

        if not isinstance(aten_op, torch._ops.OpOverload):
            raise AssertionError(
                f"Expected aten_op to be OpOverload, got {type(aten_op)}"
            )

        # Need unique name for jit function serialization
        if f.__name__ in function_name_set:
            raise AssertionError(f"Duplicated function name {f.__name__}")
        function_name_set.add(f.__name__)

        scripted_func = torch.jit.script(f)
        torch._C._jit_pass_inline(scripted_func.graph)

        for _ in range(2):
            torch._C._jit_pass_peephole(scripted_func.graph)
            torch._C._jit_pass_constant_propagation(scripted_func.graph)

        registry[str(aten_op._schema)] = scripted_func
        return f

    return decomposition_decorator


def register_decomposition(
    aten_op, registry=None, *, type="post_autograd", unsafe=False
) -> Callable[[Callable[_P, _T]], Callable[_P, _T]]:
    """
    A decorator to register a function as a decomposition to the Python
    decomposition table.  Use it like this::

        @register_decomposition(torch.ops.aten.clamp_min)
        def clamp_min(x):
            return torch.clamp(self, min=min)

    If you are writing a new decomposition, consider contributing it
    directly to PyTorch in torch._decomp.decompositions.

    This API is experimental; we are almost certainly going to extend
    the API when we make decompositions eligible for use in transforms (e.g.,
    autograd) and not just backend tracing, where we then need to know if a
    decomposition can be used to simulate a transform.

    By default, we also will register it to the Meta key of dispatcher,
    and replace the c++ Meta implementation if there is already one.

    unsafe kwarg is for reuse of this function for registering non-function
    things
    """

    if type not in {"post_autograd", "pre_autograd", "meta"}:
        raise AssertionError(
            f"type must be one of post_autograd, pre_autograd, or meta, got {type}"
        )

    def decomposition_decorator(fn: Callable[_P, _T]) -> Callable[_P, _T]:
        orig_fn = fn
        if not unsafe:
            fn = _convert_out_params(fn)

        nonlocal registry
        if registry is None:
            registry = global_decomposition_table[type]

        def register(op):
            _add_op_to_registry(registry, op, fn)

        # To handle allowing multiple aten_ops at once
        pytree.tree_map_(register, aten_op)
        return orig_fn

    return decomposition_decorator


def register_decomposition(
    ops: _GenericOperator | list[_GenericOperator],
) -> Callable[[Callable[_P, _T]], Callable[_P, _T]]:
    for op in ops if isinstance(ops, list) else [ops]:
        if op in decompositions:
            log.warning("duplicate decomp: %s", ops)
    return decomp.register_decomposition(ops, decompositions)

