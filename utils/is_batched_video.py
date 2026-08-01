
def is_batched_video(videos):
    if isinstance(videos, (list, tuple)):
        return is_valid_video(videos[0])
    elif (is_numpy_array(videos) or is_torch_tensor(videos)) and videos.ndim == 5:
        return True
    return False

