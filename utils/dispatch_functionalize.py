from typing import Any, Callable

def dispatch_functionalize(
    func: Callable[..., Any], mode: FunctionalTensorMode = FunctionalTensorMode()
) -> Callable[..., Any]:
    # TODO: pull these from aot autograd
    def to_fun(t: object) -> object:
        if isinstance(t, torch.Tensor):
            return FunctionalTensor.to_functional(t)
        return t

    def from_fun(t: object) -> object:
        if not isinstance(t, FunctionalTensor):
            # quick sanity check
            if isinstance(t, torch.Tensor):
                if torch._is_functional_tensor(t):
                    raise AssertionError(
                        "Non-FunctionalTensor torch.Tensor should not be a functional tensor"
                    )
            return t
        torch._sync(t)
        return torch._from_functional_tensor(t.elem)

    def inner(*args: Any, **kwargs: Any) -> Any:
        disable_above = torch._C._ExcludeDispatchKeyGuard(
            torch._C.DispatchKeySet(torch._C.DispatchKey.Functionalize)
        )
        with disable_above, mode:
            func_args = pytree.tree_map_only(torch.Tensor, to_fun, args)
            func_kwargs = pytree.tree_map_only(torch.Tensor, to_fun, kwargs)
            func_outputs = func(*func_args, **func_kwargs)
            outputs = pytree.tree_map_only(FunctionalTensor, from_fun, func_outputs)

            return outputs

    return inner

