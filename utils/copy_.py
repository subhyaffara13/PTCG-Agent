
def copy_(tensor: torch.Tensor, other: torch.Tensor) -> torch.Tensor:
    if not getattr(tensor, "_is_hf_initialized", False):
        with torch.no_grad():
            return tensor.copy_(other)
    return tensor


def copy_(dst, src, non_blocking=False):
    if dst is src:
        # dst.copy_(dst) can happen from the reinplacing pass
        return dst
    src = to_device(src, dst.get_device())
    src = to_dtype(src, dst.get_dtype())
    src = expand(src, dst.get_size())
    return mutate_to(dst, src)


def copy_(func, *args, **kwargs):
    _check_args_kwargs_length(args, kwargs, f"__torch_dispatch__, {func}", len_args=2)
    if not _masks_match(_maybe_get_mask(args[0]), _maybe_get_mask(args[1])):
        raise ValueError("args[0] mask and args[1] mask must match but do not")
    func(_get_data(args[0]), _get_data(args[1]))
    return args[0]


def copy_(tensor, data):
    tensor.copy_(data)

