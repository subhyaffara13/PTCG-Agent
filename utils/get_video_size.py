
def get_video_size(video: np.ndarray, channel_dim: ChannelDimension | None = None) -> tuple[int, int]:
    """
    Returns the (height, width) dimensions of the video.

    Args:
        video (`np.ndarray`):
            The video to get the dimensions of.
        channel_dim (`ChannelDimension`, *optional*):
            Which dimension the channel dimension is in. If `None`, will infer the channel dimension from the video.

    Returns:
        A tuple of the video's height and width.
    """
    if channel_dim is None:
        channel_dim = infer_channel_dimension_format(video, num_channels=(1, 3, 4))

    if channel_dim == ChannelDimension.FIRST:
        return video.shape[-2], video.shape[-1]
    elif channel_dim == ChannelDimension.LAST:
        return video.shape[-3], video.shape[-2]
    else:
        raise ValueError(f"Unsupported data format: {channel_dim}")

