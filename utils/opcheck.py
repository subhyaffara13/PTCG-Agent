from typing import Any

def opcheck(
    op: torch._ops.OpOverload | torch._ops.OpOverloadPacket | CustomOpDef,
    args: tuple[Any, ...],
    kwargs: dict[str, Any] | None = None,
    *,
    test_utils: str | Sequence[str] = _OPCHECK_DEFAULT_UTILS,
    raise_exception: bool = True,
    atol=None,
    rtol=None,
) -> dict[str, str]:
    """Given an operator and some sample arguments, tests if the operator is
    registered correctly.

    That is, when you use the torch.library/TORCH_LIBRARY APIs to create a
    custom op, you specified metadata (e.g. mutability info) about the custom op
    and these APIs require that the functions you pass them satisfy certain
    properties (e.g. no data pointer access in the fake/meta/abstract kernel)
    ``opcheck`` tests these metadata and properties.

    Concretely, we test the following:

    - test_schema: If the schema matches the implementation of
      the operator. For example: if the schema specifies a Tensor is mutated,
      then we check the implementation mutates the Tensor. If the schema
      specifies that we return a new Tensor, then we check that the
      implementation returns a new Tensor (instead of an existing one or
      a view of an existing one).
    - test_autograd_registration: If the operator supports training
      (autograd): we check that its autograd formula is registered via
      torch.library.register_autograd or a manual registration to one
      or more DispatchKey::Autograd keys. Any other DispatchKey-based
      registrations may lead to undefined behavior.
    - test_faketensor: If the operator has a FakeTensor kernel
      (and if it is correct). The FakeTensor kernel is necessary (
      but not sufficient) for the operator to work with PyTorch compilation
      APIs (torch.compile/export/FX). We check that a FakeTensor kernel
      (also sometimes known as a meta kernel) was registered for the
      operator and that it is correct. This test takes the result of
      running the operator on real tensors and the result of running
      the operator on FakeTensors and checks that they have the same
      Tensor metadata (sizes/strides/dtype/device/etc).
    - test_aot_dispatch_dynamic: If the operator has correct behavior
      with PyTorch compilation APIs (torch.compile/export/FX).
      This checks that the outputs (and gradients, if applicable) are the
      same under eager-mode PyTorch and torch.compile.
      This test is a superset of ``test_faketensor`` and is an e2e test;
      other things it tests are that the operator supports
      functionalization and that the backward pass (if it exists) also
      supports FakeTensor and functionalization.

    For best results, please call ``opcheck`` multiple times with a
    representative set of inputs. If your operator supports
    autograd, please use ``opcheck`` with inputs with ``requires_grad = True``;
    if your operator supports multiple devices (e.g. CPU and CUDA), please
    use ``opcheck`` with inputs on all supported devices.

    Args:
        op: The operator. Must either be a function decorated with
            :func:`torch.library.custom_op` or an OpOverload/OpOverloadPacket
            found in torch.ops.* (e.g. torch.ops.aten.sin, torch.ops.mylib.foo)
        args: The args to the operator
        kwargs: The kwargs to the operator
        test_utils: Tests that we should run. Default: all of them.
            Example: ("test_schema", "test_faketensor")
        raise_exception: If we should raise an exception on the first
            error. If False, we will return a dict with information
            on if each test passed or not.
        rtol (Optional[float]): Relative tolerance for floating point comparisons.
            If specified ``atol`` must also be specified.
            If omitted, default values based on the ``dtype`` are selected
            (see the table in :func:`torch.testing.assert_close`).
        atol (Optional[float]): Absolute tolerance for floating point comparisons.
            If specified ``rtol`` must also be specified.
            If omitted, default values based on the ``dtype`` are selected
            (see the table in :func:`torch.testing.assert_close`).

    .. warning::

        opcheck and :func:`torch.autograd.gradcheck` test different things;
        opcheck tests if your usage of torch.library APIs is correct while
        :func:`torch.autograd.gradcheck` tests if your autograd formula is
        mathematically correct. Use both to test custom ops that support
        gradient computation.

    Example:

        >>> # xdoctest: +REQUIRES(env:TORCH_DOCTEST_CUDA)
        >>> @torch.library.custom_op("mylib::numpy_mul", mutates_args=())
        >>> def numpy_mul(x: Tensor, y: float) -> Tensor:
        >>>     x_np = x.numpy(force=True)
        >>>     z_np = x_np * y
        >>>     return torch.from_numpy(z_np).to(x.device)
        >>>
        >>> @numpy_mul.register_fake
        >>> def _(x, y):
        >>>     return torch.empty_like(x)
        >>>
        >>> def setup_context(ctx, inputs, output):
        >>>     y, = inputs
        >>>     ctx.y = y
        >>>
        >>> def backward(ctx, grad):
        >>>     return grad * ctx.y, None
        >>>
        >>> numpy_mul.register_autograd(backward, setup_context=setup_context)
        >>>
        >>> sample_inputs = [
        >>>     (torch.randn(3), 3.14),
        >>>     (torch.randn(2, 3, device='cuda'), 2.718),
        >>>     (torch.randn(1, 10, requires_grad=True), 1.234),
        >>>     (torch.randn(64, 64, device='cuda', requires_grad=True), 90.18),
        >>> ]
        >>>
        >>> for args in sample_inputs:
        >>>     torch.library.opcheck(numpy_mul, args)

    """
    import torch.testing._internal.optests as optests

    return optests.opcheck(
        op,
        args,
        kwargs,
        test_utils=test_utils,
        raise_exception=raise_exception,
        rtol=rtol,
        atol=atol,
    )


def opcheck(
    op: torch._ops.OpOverload | torch._ops.OpOverloadPacket | CustomOpDef,
    args: tuple[Any, ...],
    kwargs: dict[str, Any] | None = None,
    *,
    test_utils: str | Sequence[str] = DEFAULT_TEST_UTILS,
    raise_exception: bool = True,
    rtol: float | None = None,
    atol: float | None = None,
) -> dict[str, str]:
    """See torch.library.opcheck for docstring"""

    if (rtol is None) ^ (atol is None):
        raise ValueError(
            "opcheck(op, ...): if you specify one of rtol/atol, you must specify both"
        )

    if kwargs is None:
        kwargs = {}
    if isinstance(op, CustomOpDef):
        op = op._opoverload
    if isinstance(op, torch._ops.OpOverloadPacket):
        op = resolve_unique_overload_or_throw(op)
    if not isinstance(op, torch._ops.OpOverload):
        raise ValueError(
            f"opcheck(op, ...): op must be instance of torch._ops.OpOverload, "
            f"e.g. torch.ops.aten.sin.default, got {type(op)}"
        )
    if test_utils == "ALL":
        test_utils = tuple(ALL_TEST_UTILS.keys())
    if isinstance(test_utils, str):
        test_utils = (test_utils,)
    if not isinstance(test_utils, (tuple, list)) or not set(test_utils).issubset(
        ALL_TEST_UTILS.keys()
    ):
        raise ValueError(
            f"opcheck(op, ..., test_utils={test_utils}), expected test_utils "
            f"to be subset of {tuple(ALL_TEST_UTILS.keys())} but it was not"
        )

    results_dict = {}
    for test_util in test_utils:
        tester = ALL_TEST_UTILS[test_util]
        try:
            tester(op, args, kwargs, rtol=rtol, atol=atol)
            results_dict[test_util] = "SUCCESS"
        except Exception as ex:
            if raise_exception:
                raise OpCheckError(
                    f"opcheck(op, ...): {test_util} failed with {ex} "
                    f"(scroll up for stack trace)"
                ) from ex
            results_dict[test_util] = ex
    return results_dict

