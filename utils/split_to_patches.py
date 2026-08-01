
def split_to_patches(pixel_values: torch.Tensor, patch_size: int, overlap_ratio: float) -> torch.Tensor:
    """Creates Patches from Batch."""
    batch_size, num_channels, height, width = pixel_values.shape

    if height == width == patch_size:
        # create patches only if scaled image is not already equal to patch size
        return pixel_values

    stride = torch_int(patch_size * (1 - overlap_ratio))

    patches = F.unfold(pixel_values, kernel_size=(patch_size, patch_size), stride=(stride, stride))
    patches = patches.permute(2, 0, 1)
    patches = patches.reshape(-1, num_channels, patch_size, patch_size)

    return patches

