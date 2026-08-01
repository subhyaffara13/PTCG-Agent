
def read_video_opencv(
    video_path: Union["URL", "Path"],
    sample_indices_fn: Callable,
    **kwargs,
) -> tuple[np.ndarray, VideoMetadata]:
    """
    Decode a video using the OpenCV backend.

    Args:
        video_path (`str`):
            Path to the video file.
        sample_indices_fn (`Callable`):
            A callable function that will return indices at which the video should be sampled. If the video has to be loaded using
            by a different sampling technique than provided by `num_frames` or `fps` arguments, one should provide their own `sample_indices_fn`.
            If not provided, simple uniform sampling with fps is performed.
            Example:
            def sample_indices_fn(metadata, **kwargs):
                return np.linspace(0, metadata.total_num_frames - 1, num_frames, dtype=int)

    Returns:
        tuple[`np.ndarray`, `VideoMetadata`]: A tuple containing:
            - Numpy array of frames in RGB (shape: [num_frames, height, width, 3]).
            - `VideoMetadata` object.
    """
    # Lazy import cv2
    requires_backends(read_video_opencv, ["cv2"])
    import cv2

    video = cv2.VideoCapture(video_path)
    total_num_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    video_fps = video.get(cv2.CAP_PROP_FPS)
    duration = total_num_frames / video_fps if video_fps else 0
    metadata = VideoMetadata(
        total_num_frames=int(total_num_frames),
        fps=float(video_fps),
        duration=float(duration),
        video_backend="opencv",
        height=int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        width=int(video.get(cv2.CAP_PROP_FRAME_WIDTH)),
    )

    indices = sample_indices_fn(metadata=metadata, **kwargs)
    index = 0
    frames = []
    while video.isOpened():
        success, frame = video.read()
        if not success:
            break
        if index in indices:
            height, width, channel = frame.shape
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(frame[0:height, 0:width, 0:channel])
        if success:
            index += 1
        if index >= total_num_frames:
            break

    video.release()
    metadata.frames_indices = indices
    return np.stack(frames), metadata

