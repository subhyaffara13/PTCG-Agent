
def read_video_pyav(
    video_path: Union["URL", "Path"],
    sample_indices_fn: Callable,
    **kwargs,
):
    """
    Decode the video with PyAV decoder.

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
        tuple[`np.array`, `VideoMetadata`]: A tuple containing:
            - Numpy array of frames in RGB (shape: [num_frames, height, width, 3]).
            - `VideoMetadata` object.
    """
    # Lazy import av
    requires_backends(read_video_pyav, ["av"])
    import av

    container = av.open(video_path)
    total_num_frames = container.streams.video[0].frames
    video_fps = container.streams.video[0].average_rate  # should we better use `av_guess_frame_rate`?
    duration = total_num_frames / video_fps if video_fps else 0
    metadata = VideoMetadata(
        total_num_frames=int(total_num_frames),
        fps=float(video_fps),
        duration=float(duration),
        video_backend="pyav",
        height=container.streams.video[0].height,
        width=container.streams.video[0].width,
    )

    indices = sample_indices_fn(metadata=metadata, **kwargs)
    frames = []
    container.seek(0)
    end_index = indices[-1]
    for i, frame in enumerate(container.decode(video=0)):
        if i > end_index:
            break
        if i >= 0 and i in indices:
            frames.append(frame)

    video = np.stack([x.to_ndarray(format="rgb24") for x in frames])
    metadata.frames_indices = indices
    return video, metadata


def read_video_pyav(container, indices):
    frames = []
    container.seek(0)
    start_index = indices[0]
    end_index = indices[-1]
    for i, frame in enumerate(container.decode(video=0)):
        if i > end_index:
            break
        if i >= start_index and i in indices:
            frames.append(frame)
    return np.stack([x.to_ndarray(format="rgb24") for x in frames])

