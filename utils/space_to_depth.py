import time

def space_to_depth(frames: torch.Tensor, temporal_block_size: int = 1, spatial_block_size: int = 1) -> torch.Tensor:
    """
    Space to depth transform. Rearranges blocks of spatial data, into depth.

    This function assumes the channels to be first, but will place the channels last after transformation.
    """
    if len(frames.shape) == 4:
        batch_size, num_channels, height, width = frames.shape
        # split up dimensions (height by spatial_block_size, width by spatial_block_size)
        frames = frames.view(
            batch_size,
            num_channels,
            height // spatial_block_size,
            spatial_block_size,
            width // spatial_block_size,
            spatial_block_size,
        )
        # move blocks to last dimension: (batch_size, H//bs, W//bs, bs, bs, C)
        frames = frames.permute(0, 2, 4, 3, 5, 1).contiguous()
        # concatenate blocks along channel dimension: (batch_size, H//bs, W//bs, bs*bs*C)
        frames = frames.view(
            batch_size,
            height // spatial_block_size,
            width // spatial_block_size,
            (spatial_block_size**2) * num_channels,
        )
        return frames
    elif len(frames.shape) == 5:
        batch_size, time, num_channels, height, width = frames.shape
        # split up dimensions (time by temporal_block_size, height by spatial_block_size, width by spatial_block_size)
        frames = frames.view(
            batch_size,
            time // temporal_block_size,
            temporal_block_size,
            num_channels,
            height // spatial_block_size,
            spatial_block_size,
            width // spatial_block_size,
            spatial_block_size,
        )
        # move blocks to last dimension: (batch_size, T//ts, H//bs, W//bs, ts, bs, bs, C)
        frames = frames.permute(0, 1, 4, 6, 2, 5, 7, 3).contiguous()
        # concatenate blocks along channel dimension: (batch_size, T//ts, H//bs, W//bs, ts*bs*bs*C)
        frames = frames.view(
            batch_size,
            time // temporal_block_size,
            height // spatial_block_size,
            width // spatial_block_size,
            temporal_block_size * (spatial_block_size**2) * num_channels,
        )
        return frames
    else:
        raise ValueError(
            "Frames should be of rank 4 (batch, channels, height, width)"
            " or rank 5 (batch, time, channels, height, width)"
        )

