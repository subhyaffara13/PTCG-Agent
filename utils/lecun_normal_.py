
def lecun_normal_(tensor):
    if not getattr(tensor, "_is_hf_initialized", False):
        _variance_scaling(tensor, mode="fan_in", distribution="truncated_normal")
    return tensor

