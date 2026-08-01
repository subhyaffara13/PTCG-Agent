
def constant_(tensor: torch.Tensor, val: float) -> torch.Tensor:
    if not getattr(tensor, "_is_hf_initialized", False):
        return TORCH_INIT_FUNCTIONS["constant_"](tensor, val=val)
    return tensor


def constant_(tensor: Tensor, val: float) -> Tensor:
    r"""Fill the input Tensor with the value :math:`\text{val}`.

    Args:
        tensor: an n-dimensional `torch.Tensor`
        val: the value to fill the tensor with

    Examples:
        >>> w = torch.empty(3, 5)
        >>> nn.init.constant_(w, 0.3)
    """
    if torch.overrides.has_torch_function_variadic(tensor):
        return torch.overrides.handle_torch_function(
            constant_, (tensor,), tensor=tensor, val=val
        )
    return _no_grad_fill_(tensor, val)


def constant_(types, args=(), kwargs=None, pg=None):
    r"""
    Fills the input ShardedTensor with the value \text{val}val.
    Args:
        tensor: tensor sharded across devices
        val: the value to fill the tensor with
    """
    validate_param(kwargs, "kwargs")
    # pyrefly: ignore [unsupported-operation]
    sharded_tensor = kwargs["tensor"]
    validate_param(sharded_tensor, "tensor")
    # pyrefly: ignore [unsupported-operation]
    val = kwargs["val"]
    validate_param(val, "val")
    for shard in sharded_tensor.local_shards():
        torch.nn.init.constant_(shard.tensor, val=val)
    return sharded_tensor

