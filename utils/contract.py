from typing import Any, Callable, Optional, Union

def contract(
    subscripts: str,
    *operands: ArrayType,
    out: ArrayType = ...,
    use_blas: bool = ...,
    optimize: OptimizeKind = ...,
    memory_limit: _MemoryLimit = ...,
    backend: BackendType = ...,
    **kwargs: Any,
) -> ArrayType: ...


def contract(
    subscripts: ArrayType,
    *operands: Union[ArrayType, Collection[int]],
    out: ArrayType = ...,
    use_blas: bool = ...,
    optimize: OptimizeKind = ...,
    memory_limit: _MemoryLimit = ...,
    backend: BackendType = ...,
    **kwargs: Any,
) -> ArrayType: ...


def contract(
    subscripts: Union[str, ArrayType],
    *operands: Union[ArrayType, Collection[int]],
    out: Optional[ArrayType] = None,
    use_blas: bool = True,
    optimize: OptimizeKind = True,
    memory_limit: _MemoryLimit = None,
    backend: BackendType = "auto",
    **kwargs: Any,
) -> ArrayType:
    """Evaluates the Einstein summation convention on the operands. A drop in
    replacement for NumPy's einsum function that optimizes the order of contraction
    to reduce overall scaling at the cost of several intermediate arrays.

    Parameters:
        subscripts: Specifies the subscripts for summation.
        *operands: These are the arrays for the operation.
        out: A output array in which set the resulting output.
        use_blas: Do you use BLAS for valid operations, may use extra memory for more intermediates.
        optimize:- Choose the type of path the contraction will be optimized with
            - if a list is given uses this as the path.
            - `'optimal'` An algorithm that explores all possible ways of
            contracting the listed tensors. Scales factorially with the number of
            terms in the contraction.
            - `'dp'` A faster (but essentially optimal) algorithm that uses
            dynamic programming to exhaustively search all contraction paths
            without outer-products.
            - `'greedy'` An cheap algorithm that heuristically chooses the best
            pairwise contraction at each step. Scales linearly in the number of
            terms in the contraction.
            - `'random-greedy'` Run a randomized version of the greedy algorithm
            32 times and pick the best path.
            - `'random-greedy-128'` Run a randomized version of the greedy
            algorithm 128 times and pick the best path.
            - `'branch-all'` An algorithm like optimal but that restricts itself
            to searching 'likely' paths. Still scales factorially.
            - `'branch-2'` An even more restricted version of 'branch-all' that
            only searches the best two options at each step. Scales exponentially
            with the number of terms in the contraction.
            - `'auto', None, True` Choose the best of the above algorithms whilst aiming to
            keep the path finding time below 1ms.
            - `'auto-hq'` Aim for a high quality contraction, choosing the best
            of the above algorithms whilst aiming to keep the path finding time
            below 1sec.
            - `False` will not optimize the contraction.

        memory_limit:- Give the upper bound of the largest intermediate tensor contract will build.
            - None or -1 means there is no limit.
            - `max_input` means the limit is set as largest input tensor.
            - A positive integer is taken as an explicit limit on the number of elements.

            The default is None. Note that imposing a limit can make contractions
            exponentially slower to perform.

        backend: Which library to use to perform the required ``tensordot``, ``transpose``
            and ``einsum`` calls. Should match the types of arrays supplied, See
            `contract_expression` for generating expressions which convert
            numpy arrays to and from the backend library automatically.

    Returns:
        The result of the einsum expression.

    Notes:
        This function should produce a result identical to that of NumPy's einsum
        function. The primary difference is ``contract`` will attempt to form
        intermediates which reduce the overall scaling of the given einsum contraction.
        By default the worst intermediate formed will be equal to that of the largest
        input array. For large einsum expressions with many input arrays this can
        provide arbitrarily large (1000 fold+) speed improvements.

        For contractions with just two tensors this function will attempt to use
        NumPy's built-in BLAS functionality to ensure that the given operation is
        performed optimally. When NumPy is linked to a threaded BLAS, potential
        speedups are on the order of 20-100 for a six core machine.
    """
    if (optimize is True) or (optimize is None):
        optimize = "auto"

    operands_list = [subscripts] + list(operands)

    # If no optimization, run pure einsum
    if optimize is False:
        return _einsum(*operands_list, out=out, **kwargs)

    # Grab non-einsum kwargs
    gen_expression = kwargs.pop("_gen_expression", False)
    constants_dict = kwargs.pop("_constants_dict", {})

    if gen_expression:
        full_str = operands_list[0]

    # Build the contraction list and operand
    contraction_list: ContractionListType
    operands, contraction_list = contract_path(  # type: ignore
        *operands_list, optimize=optimize, memory_limit=memory_limit, einsum_call=True, use_blas=use_blas
    )

    # check if performing contraction or just building expression
    if gen_expression:
        return ContractExpression(full_str, contraction_list, constants_dict, **kwargs)

    return _core_contract(operands, contraction_list, backend=backend, out=out, **kwargs)


def contract(
    state_cls: type[_TState] = _State,  # type: ignore[assignment]
) -> Callable[
    [Callable[Concatenate[_M, _P], _M]],
    _ContractFn[Concatenate[_M, _P], _M, _TState],
]:
    r"""
    Decorate a function as a composable distributed API, where the first
    argument of the function must be an :class:`nn.Module` instance or sequence
    of :class:`nn.Module` instances.

    The decorator verifies that the decorated function does not modify
    fully-qualified names (FQNs) for parameters, buffers, or modules. The
    decorated function can return different module instances than the input
    modules; the FQN invariant will be enforced following the input order.

    When a function ``func`` is decorated by ``@contract()``, a
    ``.state(module: nn.Module)`` method will be installed to the decorated
    function. Then you can retrieve and modify the state on a module by calling
    ``func.state(module)``.

    Example::
        >>> # xdoctest: +SKIP
        >>> import torch.nn as nn
        >>>
        >>> class MyModel(nn.Module):
        >>>     def __init__(self) -> None:
        >>>         super().__init__()
        >>>         self.l1 = nn.Linear(10, 10)
        >>>         self.l2 = nn.Linear(10, 10)
        >>>
        >>>     def forward(self, x):
        >>>         return self.l2(self.l1(x))
        >>>
        >>> @contract()
        >>> def my_feature(module: nn.Module) -> nn.Module:
        >>>     my_feature.state(module).some_state = "any value"
        >>>     return module
        >>>
        >>> model = MyModel()
        >>> my_feature(model.l1)
        >>> assert my_feature.state(model.l1).some_state == "any value"
        >>> my_feature(model.l2)
        >>> model(torch.randn(2, 10)).sum().backward()
    """

    # wraps will make functions decorated with contract() pickleable - needed for integration with torch.package
    @wraps(state_cls)  # type: ignore[arg-type]
    def inner(
        func: Callable[Concatenate[_M, _P], _M],
    ) -> _ContractFn[Concatenate[_M, _P], _M, _TState]:
        @wraps(func)
        def wrapper(
            module: _M,
            *args: _P.args,
            **kwargs: _P.kwargs,
        ) -> _M:
            inp_module = module
            modules: list[nn.Module]
            if isinstance(module, nn.Module):
                modules = [module]
            else:
                # If the user passes a sequence of modules, then we assume that
                # we only need to insert the state object on the root modules
                # (i.e. those without a parent) among the passed-in modules.
                # pyrefly: ignore [no-matching-overload]
                modules = _get_root_modules(list(module))
            state = state_cls()  # shared across all modules
            registry_item = RegistryItem()  # shared across all modules

            # `func` is allowed to return different module instances than the
            # input modules as long as FQNs are preserved following the input
            # module order
            all_orig_named_params: list[dict[str, nn.Parameter]] = []
            all_orig_named_buffers: list[dict[str, torch.Tensor]] = []
            all_orig_named_modules: list[dict[str, nn.Module]] = []

            for module in modules:
                default_all_state: dict[Callable, _State] = OrderedDict()
                default_registry: dict[str, RegistryItem] = OrderedDict()
                all_state: dict[Callable, _State] = module.__dict__.setdefault(  # type: ignore[call-overload]
                    STATE_KEY, default_all_state
                )
                if not isinstance(all_state, dict):
                    raise AssertionError(
                        f"Distributed composable API states corrupted: {all_state}"
                    )
                registry: dict[str, RegistryItem] = module.__dict__.setdefault(  # type: ignore[call-overload]
                    REGISTRY_KEY, default_registry
                )
                if not isinstance(registry, dict):
                    raise AssertionError(
                        f"Distributed composable API registry corrupted: {registry}"
                    )
                if func in all_state or func.__name__ in registry:
                    raise AssertionError(
                        "Each distinct composable distributed API can only be applied to a "
                        f"module once. {func.__name__} has already been applied to the "
                        f"following module:\n{module}"
                    )
                all_state.setdefault(func, state)
                registry.setdefault(func.__name__, registry_item)

                all_orig_named_params.append(OrderedDict(module.named_parameters()))
                all_orig_named_buffers.append(OrderedDict(module.named_buffers()))
                all_orig_named_modules.append(OrderedDict(module.named_modules()))

            updated = func(inp_module, *args, **kwargs)
            if updated is None:
                updated = inp_module  # type: ignore[assignment]
            updated_modules: list[nn.Module]
            if isinstance(updated, nn.Module):
                updated_modules = [updated]
            else:
                updated_modules = _get_root_modules(list(inp_module))  # type: ignore[arg-type, call-overload]

            all_new_named_params: list[dict[str, nn.Parameter]] = []
            all_new_named_buffers: list[dict[str, torch.Tensor]] = []
            all_new_named_modules: list[dict[str, nn.Module]] = []
            for module in updated_modules:
                all_new_named_params.append(OrderedDict(module.named_parameters()))
                all_new_named_buffers.append(OrderedDict(module.named_buffers()))
                all_new_named_modules.append(OrderedDict(module.named_modules()))

            num_orig_modules = len(all_orig_named_modules)
            num_new_modules = len(all_new_named_modules)
            if num_orig_modules != num_new_modules:
                raise AssertionError(
                    f"{func.__name__} should return the same number of modules as input modules"
                    f"Inputs: {num_orig_modules} modules\n"
                    f"Outputs: {num_new_modules} modules"
                )

            def check_fqn(orig_fqns: list[str], new_fqns: list[str], check_key: str):
                if orig_fqns == new_fqns:
                    return

                orig_fqn_set, new_fqn_set = set(orig_fqns), set(new_fqns)
                orig_only = orig_fqn_set - new_fqn_set
                new_only = new_fqn_set - orig_fqn_set
                if len(orig_only) or len(new_only):
                    raise RuntimeError(
                        f"{check_key}"
                        "Composable distributed API implementations cannot modify FQNs.\n"
                        f"FQNs only in original: {orig_only}\n"
                        f"FQNs only in new: {new_only}"
                    )
                else:
                    raise RuntimeError(
                        f"{check_key}"
                        "Composable distributed API implementations cannot modify "
                        "the order of FQNs.\n"
                        f"Original FQNs: {orig_only}\n"
                        f"New FQNs: {new_only}"
                    )

            for orig_named_params, new_named_params in zip(
                all_orig_named_params, all_new_named_params
            ):
                check_fqn(
                    list(orig_named_params.keys()),
                    list(new_named_params.keys()),
                    "Checking parameters: ",
                )
            for orig_named_buffers, new_named_buffers in zip(
                all_orig_named_buffers, all_new_named_buffers
            ):
                check_fqn(
                    list(orig_named_buffers.keys()),
                    list(new_named_buffers.keys()),
                    "Checking buffers: ",
                )
            for orig_named_modules, new_named_modules in zip(
                all_orig_named_modules, all_new_named_modules
            ):
                check_fqn(
                    list(orig_named_modules.keys()),
                    list(new_named_modules.keys()),
                    "Checking modules: ",
                )

            # TODO: verify that installed distributed paradigms are compatible with
            # each other.

            return updated

        def get_state(module: nn.Module) -> _State:
            return module.__dict__.setdefault(  # type: ignore[call-overload]
                STATE_KEY,
                {},  # TODO(@yhcharles): this is a temporary fix, need a better way
            ).get(func)  # type: ignore[call-overload]

        wrapper.state = get_state  # type: ignore[attr-defined]

        return wrapper  # type: ignore[return-value]

    return inner  # type: ignore[return-value]


def contract(result: _ods_ir.Type, lhs: _ods_ir.Value[_ods_ir.VectorType], rhs: _ods_ir.Value[_ods_ir.VectorType], acc: _ods_ir.Value, indexing_maps: _Union[_Sequence[_ods_ir.Attribute], _ods_ir.ArrayAttr], iterator_types: _Union[_Any, _ods_ir.ArrayAttr], *, kind: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, fastmath: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return ContractionOp(result=result, lhs=lhs, rhs=rhs, acc=acc, indexing_maps=indexing_maps, iterator_types=iterator_types, kind=kind, fastmath=fastmath, loc=loc, ip=ip).result

