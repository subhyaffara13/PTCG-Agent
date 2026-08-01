
def register_multi_grad_hook(
    tensors: Sequence[torch.Tensor],
    fn: Callable[[Sequence[torch.Tensor | None]], None]
    | Callable[[torch.Tensor], None],
    *,
    mode: Literal["all", "any"] = "all",
) -> RemovableHandle:
    r"""Register a multi-grad backward hook.

    There are two supported modes: ``"all"`` and ``"any"``.

    Under the ``"all"`` mode, the hook will be called after gradients with respect to every tensor in
    :attr:`tensors` have been computed. If a tensor is in :attr:`tensors` but
    is not part of the graph, or if a tensor is not needed to compute the gradients
    for any ``inputs`` specified for the current ``.backward()`` or ``.grad()`` call,
    this tensor will be ignored and the hook will not wait for its gradient to be
    computed.

    After every non-ignored tensor's gradient has been computed, :attr:`fn` will be
    called with those gradients. ``None`` will be passed for tensors that did not
    have their gradients computed.

    Under the ``"any"`` mode, the hook will be called after the first gradient
    with respect to a tensor in :attr:`tensors` has been computed. The hook
    will be called with that gradient as its argument.

    The hook should not modify its arguments.

    This function returns a handle with a method ``handle.remove()`` that removes the hook.

    .. note::
        See :ref:`backward-hooks-execution` for more information on how when this hook
        is executed, and how its execution is ordered relative to other hooks.

    Example::

        >>> import torch
        >>>
        >>> a = torch.rand(2, 3, requires_grad=True)
        >>> b = torch.rand(2, 3, requires_grad=True)
        >>> c = a * b
        >>> d = a * b
        >>>
        >>> def fn(grads):
        ...     print([g is not None for g in grads])
        ...
        >>> torch.autograd.graph.register_multi_grad_hook((a, b, c, d), fn)
        >>>
        >>> c.sum().backward(retain_graph=True)
        [True, True, True, False]
        >>> c.sum().backward(inputs=(a,), retain_graph=True)
        [True, False, True, False]
        >>>
    """
    supported_modes = ("all", "any")
    lock = threading.Lock()

    if mode not in supported_modes:
        raise ValueError(f"Expects mode to be one of {supported_modes} but got {mode}")

    if mode == "all":
        count: dict[int, int] = {}
        nb_calls = None
        buffer: dict[int, list[torch.Tensor | None]] = {}

        grad_fns = list(map(_get_grad_fn_or_grad_acc, tensors))
        len_tensors = len(tensors)

        def get_inner_hook(idx: int) -> Callable[[torch.Tensor], None]:
            def inner_hook(grad: torch.Tensor) -> None:
                nonlocal count, nb_calls, buffer, fn
                id = torch._C._current_graph_task_id()
                if id == -1:
                    raise AssertionError(
                        "expected this hook to be called inside a backward call"
                    )
                count[id] = count.get(id, 0)
                # pyrefly: ignore [unsupported-operation]
                buffer[id] = buffer.get(id, [None] * len_tensors)

                with lock:
                    curr_count, count[id] = count[id], count[id] + 1

                    if curr_count == 0:
                        # On the first call, compute the actual nb_calls and buffer
                        nb_calls = sum(
                            map(torch._C._will_engine_execute_node, grad_fns)
                        )

                buffer[id][idx] = grad

                if nb_calls is None:
                    raise AssertionError("Expected nb_calls to be set")
                if curr_count == nb_calls - 1:
                    fn = cast(Callable[[Sequence[torch.Tensor | None]], None], fn)
                    fn(buffer[id])
                    del count[id]
                    del buffer[id]

            return inner_hook

        handles = tuple(
            t.register_hook(get_inner_hook(i)) for i, t in enumerate(tensors)
        )
    elif mode == "any":
        fn = cast(Callable[[torch.Tensor], None], fn)
        ran_hook: dict[int, bool] = defaultdict(bool)

        @functools.wraps(fn)
        def wrapped_fn(grad: torch.Tensor) -> None:
            nonlocal ran_hook
            id = torch._C._current_graph_task_id()
            if id == -1:
                raise AssertionError(
                    "expected this hook to be called inside a backward call"
                )
            with lock:
                prev, ran_hook[id] = ran_hook[id], True
            if prev:
                return
            fn(grad)

        handles = tuple(
            tensor.register_hook(wrapped_fn)
            for tensor in tensors
            if tensor.requires_grad
        )

    return _MultiHandle(handles)  # type: ignore[possibly-undefined]

