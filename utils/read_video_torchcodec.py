from typing import Callable, Union

def read_video_torchcodec(
    video_path: Union["URL", "Path"],
    sample_indices_fn: Callable,
    **kwargs,
):
    """
    Decode the video with torchcodec decoder.

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
        Tuple[`torch.Tensor`, `VideoMetadata`]: A tuple containing:
            - Torch tensor of frames in RGB (shape: [num_frames, height, width, 3]).
            - `VideoMetadata` object.
    """
    # Lazy import torchcodec
    requires_backends(read_video_torchcodec, ["torchcodec"])
    from torchcodec.decoders import VideoDecoder

    # VideoDecoder expects a string for device, default to "cpu" if None

    decoder = VideoDecoder(
        video_path,
        # Interestingly `exact` mode takes less than approximate when we load the whole video
        seek_mode="exact",
        # Allow FFmpeg decide on the number of threads for efficiency
        num_ffmpeg_threads=0,
        device=kwargs.get("device", "cpu"),
    )
    total_num_frames = decoder.metadata.num_frames
    video_fps = decoder.metadata.average_fps
    metadata = VideoMetadata(
        total_num_frames=total_num_frames,
        fps=video_fps,
        duration=decoder.metadata.duration_seconds,
        video_backend="torchcodec",
        height=decoder.metadata.height,
        width=decoder.metadata.width,
    )

    indices = sample_indices_fn(metadata=metadata, **kwargs)
    video = decoder.get_frames_at(indices=indices).data.contiguous()
    metadata.frames_indices = indices
    return video, metadata

