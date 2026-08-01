
def video(tag, tensor, fps=4):
    tensor = make_np(tensor)
    tensor = _prepare_video(tensor)
    # If user passes in uint8, then we don't need to rescale by 255
    scale_factor = _calc_scale_factor(tensor)
    tensor = tensor.astype(np.float32)
    tensor = (tensor * scale_factor).clip(0, 255).astype(np.uint8)
    video = make_video(tensor, fps)
    return Summary(value=[Summary.Value(tag=tag, image=video)])

