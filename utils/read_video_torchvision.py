
def read_video_torchvision(
    video_path: Union["URL", "Path"],
    sample_indices_fn: Callable,
    **kwargs,
):
    """
    Decode the video with torchvision decoder.

    Args:
        video_path (`str`):
            Path to the video file.
        sample_indices_fn (`Callable`, *optional*):
            A callable function that will return indices at which the video should be sampled. If the video has to be loaded using
            by a different sampling technique than provided by `num_frames` or `fps` arguments, one should provide their own `sample_indices_fn`.
            If not provided, simple uniform sampling with fps is performed.
            Example:
            def sample_indices_fn(metadata, **kwargs):
                return np.linspace(0, metadata.total_num_frames - 1, num_frames, dtype=int)

    Returns:
        tuple[`torch.Tensor`, `VideoMetadata`]: A tuple containing:
            - Torch tensor of frames in RGB (shape: [num_frames, height, width, 3]).
            - `VideoMetadata` object.
    """
    warnings.warn(
        "Using `torchvision` for video decoding is deprecated and will be removed in future versions. "
        "Please use `torchcodec` instead."
    )
    video, _, info = torchvision_io.read_video(
        video_path,
        start_pts=0.0,
        end_pts=None,
        pts_unit="sec",
        output_format="TCHW",
    )
    video_fps = info["video_fps"]
    total_num_frames = video.size(0)
    duration = total_num_frames / video_fps if video_fps else 0
    metadata = VideoMetadata(
        total_num_frames=int(total_num_frames),
        fps=float(video_fps),
        duration=float(duration),
        video_backend="torchvision",
    )

    indices = sample_indices_fn(metadata=metadata, **kwargs)
    video = video[indices].contiguous()
    metadata.update(
        {
            "frames_indices": indices,
            "height": video.shape[2],
            "width": video.shape[3],
        }
    )
    return video, metadata

