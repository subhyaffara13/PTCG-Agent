
def reorder_videos(
    processed_videos: dict[tuple[int, int], "torch.Tensor"],
    grouped_videos_index: dict[int, tuple[tuple[int, int], int]],
) -> list["torch.Tensor"]:
    """
    Reconstructs a list of videos in the original order.
    """
    return [
        processed_videos[grouped_videos_index[i][0]][grouped_videos_index[i][1]]
        for i in range(len(grouped_videos_index))
    ]

