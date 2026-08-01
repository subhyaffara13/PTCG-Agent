
def group_videos_by_shape(
    videos: list["torch.Tensor"],
) -> tuple[dict[tuple[int, int], "torch.Tensor"], dict[int, tuple[tuple[int, int], int]]]:
    """
    Groups videos by shape.
    Returns a dictionary with the shape as key and a list of videos with that shape as value,
    and a dictionary with the index of the video in the original list as key and the shape and index in the grouped list as value.
    """
    grouped_videos = {}

    grouped_videos_index = {}
    for i, video in enumerate(videos):
        shape = video.shape[-2::]
        num_frames = video.shape[-4]  # video format BTCHW
        shape = (num_frames, *shape)
        if shape not in grouped_videos:
            grouped_videos[shape] = []
        grouped_videos[shape].append(video)
        grouped_videos_index[i] = (shape, len(grouped_videos[shape]) - 1)

    # stack videos with the same size and number of frames
    grouped_videos = {shape: torch.stack(videos, dim=0) for shape, videos in grouped_videos.items()}
    return grouped_videos, grouped_videos_index

