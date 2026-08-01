
def triton_op(
    name: str,
    fn: Callable | None = None,
    /,
    *,
    mutates_args: str | Iterable[str],
    schema: str | None = None,
) -> Callable:
    """Create a custom operator whose implementation is backed by 1+ triton kernels.

    This is a more structured way of using triton kernels with PyTorch.
    Prefer using triton kernels with no ``torch.library`` custom operator wrappers
    (like :func:`torch.library.custom_op`, :func:`torch.library.triton_op`) because
    that is simpler;
    only use :func:`torch.library.custom_op`/:func:`torch.library.triton_op` if you
    want to create an operator that behaves like PyTorch built-in operators.
    For example, you may use a ``torch.library`` wrapper API to define the
    behavior of the triton kernel when passed a tensor subclass or under
    a TorchDispatchMode.

    Use :func:`torch.library.triton_op` instead of :func:`torch.library.custom_op`
    when the implementation
    consists of 1+ triton kernels. :func:`torch.library.custom_op` treats
    custom operators as opaque (:func:`torch.compile` and
    :func:`torch.export.export` will never trace into them), but ``triton_op``
    makes the implementation visible to these subsystems, allowing them
    to optimize the triton kernel(s).

    Note that ``fn`` must only consist of calls to PyTorch-understood
    operators and triton kernels. Any triton kernels called inside ``fn``
    must be wrapped in a call to :func:`torch.library.wrap_triton`.

    Args:
        name (str): A name for the custom op that looks like "{namespace}::{name}",
            e.g. "mylib::my_linear". The name is used as the op's stable identifier
            in PyTorch subsystems (e.g. torch.export, FX graphs).
            To avoid name collisions, please use your project name as the namespace;
            e.g. all custom ops in pytorch/fbgemm use "fbgemm" as the namespace.
        mutates_args (Iterable[str] or "unknown"): The names of args that the function mutates.
            This MUST be accurate, otherwise, the behavior is undefined. If "unknown",
            it pessimistically assumes that all inputs to the operator are being mutated.
        schema (str | None): A schema string for the operator. If None
            (recommended) we'll infer a schema for the operator from its type
            annotations. We recommend letting us infer a schema unless you
            have a specific reason not to.
            Example: "(Tensor x, int y) -> (Tensor, Tensor)".

    Example::

        >>> # xdoctest: +REQUIRES(env:TORCH_DOCTEST_CUDA)
        >>> import torch
        >>> from torch.library import triton_op, wrap_triton
        >>>
        >>> import triton
        >>> from triton import language as tl
        >>>
        >>> @triton.jit
        >>> def add_kernel(
        >>>     in_ptr0,
        >>>     in_ptr1,
        >>>     out_ptr,
        >>>     n_elements,
        >>>     BLOCK_SIZE: "tl.constexpr",
        >>> ):
        >>>     pid = tl.program_id(axis=0)
        >>>     block_start = pid * BLOCK_SIZE
        >>>     offsets = block_start + tl.arange(0, BLOCK_SIZE)
        >>>     mask = offsets < n_elements
        >>>     x = tl.load(in_ptr0 + offsets, mask=mask)
        >>>     y = tl.load(in_ptr1 + offsets, mask=mask)
        >>>     output = x + y
        >>>     tl.store(out_ptr + offsets, output, mask=mask)
        >>>
        >>> @triton_op("mylib::add", mutates_args={})
        >>> def add(x: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
        >>>     output = torch.empty_like(x)
        >>>     n_elements = output.numel()
        >>>
        >>>     def grid(meta):
        >>>         return (triton.cdiv(n_elements, meta["BLOCK_SIZE"]),)
        >>>
        >>>     # NB: we need to wrap the triton kernel in a call to wrap_triton
        >>>     wrap_triton(add_kernel)[grid](x, y, output, n_elements, 16)
        >>>     return output
        >>>
        >>> @torch.compile
        >>> def f(x, y):
        >>>     return add(x, y)
        >>>
        >>> x = torch.randn(3, device="cuda")
        >>> y = torch.randn(3, device="cuda")
        >>>
        >>> z = f(x, y)
        >>> assert torch.allclose(z, x + y)

    """

    def dec(fn: Callable[..., object]) -> CustomOpDef:
        def backend_fn(*args, **kwargs):  # type: ignore[no-untyped-def]
            # Optimization: we're passing regular Tensors into the triton kernel, so
            # no need to go through HOP dispatch
            with set_wrap_triton_enabled(False):
                return fn(*args, **kwargs)

        result = custom_op(
            name,
            backend_fn,
            mutates_args=mutates_args,
            schema=infer_schema(fn, mutates_args=mutates_args),
        )
        from .._subclasses.functional_tensor import FunctionalTensorMode

        # We require that the user pass us a function that is make_fx traceable,
        # so we can just register it as the Fake/meta kernel.
        result.register_fake(fn)

        # We decompose the operator when FunctionalTensorMode is active.
        # The goal is to decompose the operator in AOTDispatcher.
        # - With torch.compile, this means that the backend (usually Inductor)
        #   can see a call to the triton kernel(s) and so it can directly optimize
        #   them by inlining them into the lowering process.
        def functional_decomp(  # type: ignore[no-untyped-def]
            mode, op, types, args, kwargs
        ):
            # NOTE [Export custom triton op]
            # For torch.export (strict and non-strict), we don't do functional decomposition.
            # Instead, we preserve the custom triton ops as custom ops. This is because we want
            # the exported program to be high-level and serializable. If we decompose
            # the custom op to a functional hop and make it a node in exported program,
            # we need to figure out ways of serializing the hop and its arguments, which can be triton.jited
            # functions and triton dtypes. This is undesirable because:
            # - it can be tedious to maintain a layer that serializes the jited function (e.g. with a string) and dtypes.
            # - exported program will contain the implementation detail (e.g. triton source code) for a specific
            #   backend (GPU), which is probably at a wrong level of abstraction.
            # - changes to triton or the serialization logic for triton arguments can be BC breaking
            #
            # In the short term, we expect users to have a separate aot_compile stage that compiles the exported program
            # into a Cubin file on the same machine that users call export, which does autotuning and removes triton
            # dependency and serve the model with Cubin. This guarantees that triton changes won't break BC.
            # In the long term, we may export multiple cubins for the triton op directly
            from torch.export._trace import custom_triton_ops_decomposition_disabled

            if custom_triton_ops_decomposition_disabled():
                return mode.__torch_dispatch__(op, types, args, kwargs)
            else:
                # TODO: https://github.com/pytorch/pytorch/issues/160333
                # We should deduplicate the unrecognized_types logic.
                import torch._subclasses

                unrecognized_types = [
                    t
                    for t in types
                    if not issubclass(t, torch._subclasses.FakeTensor)
                    and t
                    not in [
                        torch.Tensor,
                        torch._subclasses.functional_tensor.FunctionalTensor,
                    ]
                ]

                if unrecognized_types:
                    return NotImplemented
                with mode:
                    return fn(*args, **kwargs)

        triton_kernels = get_inner_triton_kernels(fn)
        triton_ops_to_kernels[name] = triton_kernels
        result.register_torch_dispatch(FunctionalTensorMode, functional_decomp)
        return result

    if fn is None:
        return dec
    else:
        return dec(fn)

