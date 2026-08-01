
def unpatchify(tensor: torch.Tensor, patch_height: int, patch_width: int) -> torch.Tensor:
    batch_size = tensor.shape[0]
    patch_size = int((tensor.shape[-1] / 3) ** 0.5)
    if patch_height * patch_width != tensor.shape[1]:
        raise ValueError(
            f"Number of patches {tensor.shape[1]} does not match patch height ({patch_height}) and width ({patch_width})."
        )

    tensor = tensor.reshape(shape=(batch_size, patch_height, patch_width, patch_size, patch_size, 3))
    tensor = tensor.permute(0, 5, 1, 3, 2, 4)
    tensor = tensor.reshape(shape=(batch_size, 3, patch_height * patch_size, patch_width * patch_size))

    return tensor

