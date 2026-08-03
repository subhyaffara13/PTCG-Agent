import functools
from typing import Callable

def once_differentiable(
    fn: Callable[Concatenate[_T, _P], _R],
) -> Callable[Concatenate[_T, _P], _R]:
    @functools.wraps(fn)
    def wrapper(ctx: _T, *args: _P.args, **kwargs: _P.kwargs) -> _R:
        with torch.no_grad():
            outputs = fn(ctx, *args, **kwargs)

        if not torch.is_grad_enabled():
            return outputs

        # If any of the inputs have requires_grad=True, we force the outputs
        # to have requires_grad=True but point to a grad_fn which throws an
        # error message during (double) back-propagation.
        # XXX: this is only an approximation of requires_grad - there's no way
        # to figure out if fn didn't use ctx.saved_tensors and as a result
        # some Tensors might require grad, even if no args do.
        # Unfortunately, this leads to unexpected error messages ("no nodes
        # require computing gradients"), but I don't have a better idea.
        # These functions would raise an error in backward anyway.
        requires_grad = any(
            isinstance(arg, torch.Tensor) and arg.requires_grad for arg in args
        )
        if not requires_grad:
            return outputs

        if not isinstance(outputs, tuple):
            outputs_ = (outputs,)
        else:
            outputs_ = outputs

        err_fn = _functions.DelayedError(
            b"trying to differentiate twice a function that was marked "
            b"with @once_differentiable",
            len(outputs_),
        )

        # Create aliases of each output that has requires_grad=True. We need
        # at least one of the inputs to err_fn to require grad so that the
        # output will have a grad_fn.
        def fake_requires_grad(var):
            if var is not None:
                var = var.detach()
                var.requires_grad = True
            return var

        return err_fn(*[fake_requires_grad(v) for v in outputs_])  # type: ignore[return-value]

    return wrapper

