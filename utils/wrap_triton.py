from typing import Any, Callable

def wrap_triton(triton_kernel: Callable, /) -> Any:
    """Allows capture of a triton kernel into a graph via make_fx or
    non-strict ``torch.export``.

    These technologies perform Dispatcher-based tracing (via
    ``__torch_dispatch__``) and cannot see calls to raw triton kernels.
    The ``wrap_triton`` API wraps a triton kernel into a callable that
    can actually be traced into a graph.

    Please use this API together with :func:`torch.library.triton_op`.

    Examples:

        >>> # xdoctest: +SKIP
        >>> import torch
        >>> import triton
        >>> from triton import language as tl
        >>> from torch.fx.experimental.proxy_tensor import make_fx
        >>> from torch.library import wrap_triton
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
        >>> def add(x, y):
        >>>     output = torch.empty_like(x)
        >>>     n_elements = output.numel()
        >>>
        >>>     def grid_fn(meta):
        >>>         return (triton.cdiv(n_elements, meta["BLOCK_SIZE"]),)
        >>>
        >>>     wrap_triton(add_kernel)[grid_fn](x, y, output, n_elements, 16)
        >>>     return output
        >>>
        >>> x = torch.randn(3, device="cuda")
        >>> y = torch.randn(3, device="cuda")
        >>> gm = make_fx(add)(x, y)
        >>> print(gm.code)
        >>> # def forward(self, x_1, y_1):
        >>> #     empty_like = torch.ops.aten.empty_like.default(x_1, pin_memory = False)
        >>> #     triton_kernel_wrapper_mutation_proxy = triton_kernel_wrapper_mutation(
        >>> #         kernel_idx = 0, constant_args_idx = 0,
        >>> #         grid = [(1, 1, 1)], kwargs = {
        >>> #             'in_ptr0': x_1, 'in_ptr1': y_1, 'out_ptr': empty_like,
        >>> #             'n_elements': 3, 'BLOCK_SIZE': 16
        >>> #         })
        >>> #     return empty_like

    """
    from triton.runtime.autotuner import Autotuner
    from triton.runtime.jit import JITFunction

    from torch._higher_order_ops.triton_kernel_wrap import TraceableTritonKernelWrapper

    if not isinstance(triton_kernel, (JITFunction, Autotuner)):
        raise RuntimeError(
            "wrap_triton only works on functions annotated with triton.jit or triton.autotune"
        )
    if not is_wrap_triton_enabled():
        return triton_kernel
    return TraceableTritonKernelWrapper(triton_kernel, None, None)

