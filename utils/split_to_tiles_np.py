
def split_to_tiles_np(image: np.ndarray, num_tiles_height: int, num_tiles_width: int) -> np.ndarray:
    """Split an image into tiles (numpy version)."""
    num_channels, height, width = image.shape
    tile_height = height // num_tiles_height
    tile_width = width // num_tiles_width

    image = image.reshape(num_channels, num_tiles_height, tile_height, num_tiles_width, tile_width)
    image = image.transpose(1, 3, 0, 2, 4)
    image = image.reshape(num_tiles_width * num_tiles_height, num_channels, tile_height, tile_width)

    return np.ascontiguousarray(image)

