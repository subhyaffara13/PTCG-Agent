
def is_valid_video_frame(frame):
    return isinstance(frame, PIL.Image.Image) or (
        (is_numpy_array(frame) or is_torch_tensor(frame)) and frame.ndim == 3
    )

