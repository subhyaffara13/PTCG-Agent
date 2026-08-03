from typing import Callable

def autograd_not_implemented(custom_op):
    def kernel(*args, **kwargs):
        if torch.is_grad_enabled() and pytree.tree_any(
            lambda x: isinstance(x, torch.Tensor) and x.requires_grad, (args, kwargs)
        ):
            raise RuntimeError("Autograd has not been implemented for operator")
        with torch._C._AutoDispatchBelowAutograd():
            return custom_op(*args, **kwargs)

    return kernel


def autograd_not_implemented(op: OperatorBase, deferred_error: bool) -> Callable:
    def inner(*args, **kwargs):
        return autograd_not_implemented_inner(op, deferred_error, *args, **kwargs)

    return inner

