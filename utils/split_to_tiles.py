
def split_to_tiles(images: "torch.Tensor", num_tiles_height: int, num_tiles_width: int) -> "torch.Tensor":
    # Split image into number of required tiles (width x height)
    batch_size, num_channels, height, width = images.size()
    images = images.view(
        batch_size,
        num_channels,
        num_tiles_height,
        height // num_tiles_height,
        num_tiles_width,
        width // num_tiles_width,
    )
    # Permute dimensions to reorder the axes
    image = images.permute(0, 2, 4, 1, 3, 5).contiguous()
    # Reshape into the desired output shape (batch_size * 4, num_channels, width/2, height/2)
    image = image.view(
        batch_size,
        num_tiles_width * num_tiles_height,
        num_channels,
        height // num_tiles_height,
        width // num_tiles_width,
    )
    return image

