
def get_uniform_frame_indices(total_num_frames: int, num_frames: int | None = None):
    """
    Creates a numpy array for uniform sampling of `num_frame` frames from `total_num_frames`
    when loading a video.

    Args:
        total_num_frames (`int`):
            Total number of frames that a video has.
        num_frames (`int`, *optional*):
            Number of frames to sample uniformly. If not specified, all frames are sampled.

    Returns:
        np.ndarray: np array of frame indices that will be sampled.
    """
    if num_frames is not None:
        indices = np.arange(0, total_num_frames, total_num_frames / num_frames).astype(int)
    else:
        indices = np.arange(0, total_num_frames).astype(int)
    return indices

