
def pad_to_max_patches(
    video: "torch.Tensor", positions: "torch.Tensor", target_length: int
) -> tuple["torch.Tensor", "torch.Tensor"]:
    """
    Pad the video along to max number of patches
    """
    current_length = video.shape[1]
    padding_length = target_length - current_length
    if padding_length > 0:
        padding = [0, 0, 0, padding_length, 0, 0]
        pos_padding = (0, 0, 0, padding_length, 0, 0)
        video = torch.nn.functional.pad(video, padding, mode="constant", value=0)
        positions = torch.nn.functional.pad(positions, pos_padding, mode="constant", value=-1)
    return video, positions


def pad_to_max_patches(
    video: "torch.Tensor", positions: "torch.Tensor", target_length: int
) -> tuple["torch.Tensor", "torch.Tensor"]:
    """
    Pad the video along to max number of patches
    """
    current_length = video.shape[1]
    padding_length = target_length - current_length
    if padding_length > 0:
        padding = [0, 0, 0, padding_length, 0, 0]
        pos_padding = (0, 0, 0, padding_length, 0, 0)
        video = torch.nn.functional.pad(video, padding, mode="constant", value=0)
        positions = torch.nn.functional.pad(positions, pos_padding, mode="constant", value=-1)
    return video, positions

