from typing import Callable, Union

def read_video_decord(
    video_path: Union["URL", "Path"],
    sample_indices_fn: Callable,
    **kwargs,
):
    """
    Decode a video using the Decord backend.

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
        tuple[`np.array`, `VideoMetadata`]: A tuple containing:
            - Numpy array of frames in RGB (shape: [num_frames, height, width, 3]).
            - `VideoMetadata` object.
    """
    # Lazy import from decord
    requires_backends(read_video_decord, ["decord"])
    from decord import VideoReader, cpu

    vr = VideoReader(uri=video_path, ctx=cpu(0))  # decord has problems with gpu
    video_fps = vr.get_avg_fps()
    total_num_frames = len(vr)
    duration = total_num_frames / video_fps if video_fps else 0
    metadata = VideoMetadata(
        total_num_frames=int(total_num_frames),
        fps=float(video_fps),
        duration=float(duration),
        video_backend="decord",
    )

    indices = sample_indices_fn(metadata=metadata, **kwargs)
    video = vr.get_batch(indices).asnumpy()

    metadata.update(
        {
            "frames_indices": indices,
            "height": video.shape[1],
            "width": video.shape[2],
        }
    )
    return video, metadata

