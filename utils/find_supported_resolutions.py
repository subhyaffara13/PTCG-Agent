
def find_supported_resolutions(max_num_chunks: int, patch_size: SizeDict) -> torch.Tensor:
    """
    Computes all of the allowed resolutions for a fixed number of chunks
    and patch_size. Useful for when dividing an image into chunks.

    Args:
        max_num_chunks (int): Maximum number of chunks for processing.
        patch_size (int): Size of the side of the patch.

    Returns:
        torch.Tensor: List of possible resolutions as tuples (height, width).

    Example:
        >>> max_num_chunks = 5
        >>> patch_size = 224
        >>> find_supported_resolutions(max_num_chunks, patch_size)
        tensor([(224, 896), (448, 448), (224, 224), (896, 224), (224, 672),
        (672, 224), (224, 448), (448, 224)])

        Given max_num_chunks=4, patch_size=224, it will create a dictionary:
        {
        0.25: [(1, 4)],
        1.0: [(2, 2), (1, 1)],
        4.0: [(4, 1)],
        0.33: [(1, 3)],
        3.0: [(3, 1)],
        0.5: [(1, 2)],
        2.0: [(2, 1)]
        }

        and return the resolutions multiplied by the patch_size:
        [(1*224, 4*224), (2*224, 2*224), ..., (2*224, 1*224)]
    """
    height, width = patch_size.height, patch_size.width
    if height != width:
        raise ValueError("`size` must be square.")

    patch_size = height

    asp_dict = defaultdict(list)
    for chunk_size in range(max_num_chunks, 0, -1):
        _factors = sorted(get_factors(chunk_size))
        _asp_ratios = [(factor, chunk_size // factor) for factor in _factors]
        for height, width in _asp_ratios:
            ratio_float = height / width
            asp_dict[ratio_float].append((height, width))

    # get the resolutions multiplied by the patch_size
    possible_resolutions = []
    for value in asp_dict.values():
        for height, depth in value:
            possible_resolutions.append((height * patch_size, depth * patch_size))

    return possible_resolutions

