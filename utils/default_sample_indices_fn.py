
def default_sample_indices_fn(metadata: VideoMetadata, num_frames=None, fps=None, **kwargs):
    """
    A default sampling function that replicates the logic used in get_uniform_frame_indices,
    while optionally handling `fps` if `num_frames` is not provided.

    Args:
        metadata (`VideoMetadata`):
            `VideoMetadata` object containing metadata about the video, such as "total_num_frames" or "fps".
        num_frames (`int`, *optional*):
            Number of frames to sample uniformly.
        fps (`int` or `float`, *optional*):
            Desired frames per second. Takes priority over num_frames if both are provided.

    Returns:
        `np.ndarray`: Array of frame indices to sample.
    """
    total_num_frames = metadata.total_num_frames
    video_fps = metadata.fps

    # If num_frames is not given but fps is, calculate num_frames from fps
    if num_frames is None and fps is not None:
        num_frames = int(total_num_frames / video_fps * fps)
        if num_frames > total_num_frames:
            raise ValueError(
                f"When loading the video with fps={fps}, we computed num_frames={num_frames} "
                f"which exceeds total_num_frames={total_num_frames}. Check fps or video metadata."
            )

    if num_frames is not None:
        indices = np.arange(0, total_num_frames, total_num_frames / num_frames, dtype=int)
    else:
        indices = np.arange(0, total_num_frames, dtype=int)
    return indices

