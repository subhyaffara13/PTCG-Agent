
def _create_differentiable(inps: Any, level: int | None = None) -> Any:
    def create_differentiable(x: torch.Tensor | Any) -> torch.Tensor:
        if isinstance(x, torch.Tensor):
            with enable_inplace_requires_grad(True):
                return _set_tensor_requires_grad(x)
        raise ValueError(f"Thing passed to transform API must be Tensor, got {type(x)}")

    return tree_map(create_differentiable, inps)

