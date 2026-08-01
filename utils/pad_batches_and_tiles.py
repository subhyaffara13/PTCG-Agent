
def pad_batches_and_tiles(
    batch_images: list[list["torch.Tensor"]],
    max_image_tiles: int,
) -> tuple["torch.Tensor", list[list[int]]]:
    """
    Stack a list of lists of images with variable lengths into a torch.Tensor, applying zero padding as needed.
    Each list in the input represents a batch sample, and each image within a list is expected to be
    pre-split into tiles. The resulting array will have a shape of
    (batch_size, max_num_images, max_image_tiles, channels, tile_height, tile_width).

    Args:
        batch_images (`List[List[torch.Tensor]]`):
            A list of lists of image tiles. Each inner list represents
            a batch sample containing multiple images, where each image is pre-split into tiles.
            The shape of each tile array is (num_tiles, channels, tile_height, tile_width).
        max_image_tiles (int):
            The maximum number of tiles any image was potantially split.

    Returns:
        `Tuple[torch.Tensor, List[List[int]]]`: A tuple containing:
            - stacked_images (`torch.Tensor`):
                A numpy array of stacked images with shape
                (batch_size, max_num_images, max_image_tiles, channels, tile_height, tile_width).
            - all_num_tiles (`List[List[int]]`):
                A list of lists containing the number of tiles
                for each image in each batch sample.
    """
    # Determine output shape
    batch_size = len(batch_images)
    max_num_images = max(len(images) for images in batch_images)
    shapes = [image.shape for images in batch_images for image in images]
    _, channels, tile_height, tile_width = shapes[0]

    # Initialize the stacked images array with zeros
    stacked_images = torch.zeros(
        (batch_size, max_num_images, max_image_tiles, channels, tile_height, tile_width),
        dtype=torch.float32,
        device=batch_images[0][0].device,
    )

    # Fill the stacked images array with the tiled images from the batch
    all_num_tiles = []
    for i, images in enumerate(batch_images):
        num_sample_tiles = []
        for j, image in enumerate(images):
            num_tiles = image.shape[0]
            stacked_images[i, j, :num_tiles] = image
            num_sample_tiles.append(num_tiles)
        all_num_tiles.append(num_sample_tiles)

    return stacked_images, all_num_tiles

