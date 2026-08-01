
def make_eager_backend_with_torch_function_modes(
    modes: Iterable[torch.overrides.TorchFunctionMode],
) -> Callable[..., Any]:
    """Used to trace HOPs (cond and while) for eager execution, the metadata
    TF mode mutates vars outside of the scope of the HOP, and we can't have graph breaks
    in the HOP, so we need to externally run this mode and not trace it."""
    from contextlib import ExitStack

    def fn(
        gm: torch.fx.GraphModule, fake_tensor_inputs: list[torch.Tensor], **kwargs: Any
    ) -> Callable[..., Any]:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            with ExitStack() as stack:
                for mode in modes:
                    stack.enter_context(mode)
                return gm.forward(*args, **kwargs)

        return wrapper

    return fn

