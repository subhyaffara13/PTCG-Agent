
def patchify(tensor: torch.Tensor, patch_size: int) -> torch.Tensor:
    batch_size, num_channels, height, width = tensor.shape
    patch_height = height // patch_size
    patch_width = width // patch_size

    tensor = tensor.reshape(shape=(batch_size, num_channels, patch_height, patch_size, patch_width, patch_size))
    tensor = tensor.permute(0, 2, 4, 3, 5, 1)
    tensor = tensor.reshape(shape=(batch_size, patch_height * patch_width, patch_size**2 * 3))

    return tensor

