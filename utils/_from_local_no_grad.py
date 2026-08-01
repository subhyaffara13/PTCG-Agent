
def _from_local_no_grad(
    local_tensor: torch.Tensor,
    sharding_spec: DTensorSpec,
) -> DTensor:
    """
    This method is similar to ``DTensor.from_local()`` except that in eager mode
    it avoids some CPU overhead by avoiding default args and not being differentiable.
    """
    # pyrefly: ignore [bad-argument-type]
    return DTensor(
        # Use the local tensor directly instead of constructing a new tensor
        # variable, e.g. with `view_as()`, since this is not differentiable
        # pyrefly: ignore [bad-argument-count]
        local_tensor,
        sharding_spec,
        # pyrefly: ignore [unexpected-keyword]
        requires_grad=local_tensor.requires_grad,
    )

