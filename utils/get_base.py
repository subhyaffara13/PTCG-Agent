
def get_base(tensor):
    if torch.is_inference_mode_enabled():
        return tensor._inference_mode_base
    else:
        return tensor._base

