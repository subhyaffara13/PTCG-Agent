from typing import Optional

def convert_aspect_ratios_to_ids(
    aspect_ratios: list[list[tuple[int, int]]],
    max_image_tiles: int,
    device: Optional["torch.device"] = None,
) -> "torch.Tensor":
    """
    Convert aspect ratio tuples to unique ids.

    For batch padding we use 0, because there might be different number of images in each batch.
    The aspect ratio ids start from 1, with 1 corresponding to the first supported aspect ratio.

    Args:
        aspect_ratios (`List[List[Tuple[int, int]]]`):
            A list of aspect ratios for each image in the batch.
        max_image_tiles (`int`):
            The maximum number of tiles any image can be split into.
        device (`torch.device`, *optional*):
            The device to create the tensor on. Defaults to CPU.

    Returns:
        `torch.Tensor`:
            The aspect ratios ids as a numpy array with shape (batch_size, max_num_images).
            Each id corresponds to the index of the aspect ratio in the list of supported aspect ratios,
            offset by 1 (so 0 can be used for padding).
    """
    batch_size = len(aspect_ratios)
    max_num_images = max(len(row) for row in aspect_ratios)
    supported_aspect_ratios = get_all_supported_aspect_ratios(max_image_tiles)

    aspect_ratios_ids = torch.zeros((batch_size, max_num_images), dtype=torch.long, device=device)
    for i, sample_aspect_ratios in enumerate(aspect_ratios):
        for j, (num_tiles_h, num_tiles_w) in enumerate(sample_aspect_ratios):
            aspect_ratios_ids[i, j] = supported_aspect_ratios.index((num_tiles_h, num_tiles_w)) + 1
    return aspect_ratios_ids

