
def convert_sparse_cross_attention_mask_to_dense(
    cross_attention_token_mask: list[list[list[int]]],
    num_tiles: list[list[int]],
    max_num_tiles: int,
    length: int,
) -> np.ndarray:
    """
    Convert the cross attention mask indices to a cross attention mask 4D array.

    This function takes a sparse representation of cross attention masks and converts it to a dense 4D numpy array.
    The sparse representation is a nested list structure that defines attention ranges for each image in each batch item.

    Args:
        cross_attention_token_mask (list[list[list[int]]]): A nested list structure where:
            - The outer list represents the batch dimension.
            - The middle list represents different images within each batch item.
            - The inner list contains pairs of integers [start, end] representing token ranges for each image.
        num_tiles (list[list[int]]): A nested list structure specifying the number of tiles for each image in each batch item.
        max_num_tiles (int): The maximum possible number of tiles.
        length (int): The total sequence length of the input.

    Returns:
        np.ndarray: A 4D numpy array of shape (batch_size, length, max_num_images, max_num_tiles)
            The array contains `1` where attention is allowed and `0` where it is not.

    Note:
        - Special handling is done for cases where the end token is -1, which is interpreted as attending to the end of the sequence.
    """

    batch_size = len(cross_attention_token_mask)
    max_num_images = max(len(masks) for masks in cross_attention_token_mask)

    cross_attention_mask = np.zeros(
        shape=(batch_size, length, max_num_images, max_num_tiles),
        dtype=np.int64,
    )

    for sample_idx, (sample_masks, sample_num_tiles) in enumerate(zip(cross_attention_token_mask, num_tiles)):
        for mask_idx, (locations, mask_num_tiles) in enumerate(zip(sample_masks, sample_num_tiles)):
            if len(locations) == 2:
                start, end = locations
                end = min(end, length)
                if end == -1:
                    end = length
                cross_attention_mask[sample_idx, start:end, mask_idx, :mask_num_tiles] = 1
    return cross_attention_mask

