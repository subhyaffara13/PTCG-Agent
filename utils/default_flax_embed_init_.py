
def default_flax_embed_init_(tensor):
    if not getattr(tensor, "_is_hf_initialized", False):
        _variance_scaling(tensor, mode="fan_in", distribution="normal")
    return tensor

