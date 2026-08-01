
def torch_extract_patches(image_tensor, patch_height, patch_width):
    """
    Utility function to extract patches from a given tensor representing a batch of images. Returns a tensor of shape
    (batch_size, `rows`, `columns`, `num_channels` x `patch_height` x `patch_width`).

    Args:
        image_tensor (torch.Tensor):
            The image tensor to extract patches from.
        patch_height (int):
            The height of the patches to extract.
        patch_width (int):
            The width of the patches to extract.
    """
    patches = torch.nn.functional.unfold(image_tensor, (patch_height, patch_width), stride=(patch_height, patch_width))
    patches = patches.reshape(image_tensor.size(0), image_tensor.size(1), patch_height, patch_width, -1)
    patches = patches.permute(0, 4, 2, 3, 1).reshape(
        image_tensor.size(0),
        image_tensor.size(2) // patch_height,
        image_tensor.size(3) // patch_width,
        image_tensor.size(1) * patch_height * patch_width,
    )
    return patches


def torch_extract_patches(image_tensor, patch_height, patch_width):
    """
    Utility function to extract patches from a given tensor representing a batch of images. Returns a tensor of shape
    (batch_size, `rows`, `columns`, `num_channels` x `patch_height` x `patch_width`).

    Args:
        image_tensor (torch.Tensor):
            The image tensor to extract patches from.
        patch_height (int):
            The height of the patches to extract.
        patch_width (int):
            The width of the patches to extract.
    """
    patches = torch.nn.functional.unfold(image_tensor, (patch_height, patch_width), stride=(patch_height, patch_width))
    patches = patches.reshape(image_tensor.size(0), image_tensor.size(1), patch_height, patch_width, -1)
    patches = patches.permute(0, 4, 2, 3, 1).reshape(
        image_tensor.size(0),
        image_tensor.size(2) // patch_height,
        image_tensor.size(3) // patch_width,
        image_tensor.size(1) * patch_height * patch_width,
    )
    return patches


def torch_extract_patches(image_tensor, patch_height, patch_width):
    """
    Extract patches from image tensor. Returns tensor of shape (batch, rows, columns, patch_height*patch_width*channels).

    Args:
        image_tensor (`torch.Tensor`):
            Image tensor of shape (batch, channels, height, width).
        patch_height (`int`):
            Height of patches to extract.
        patch_width (`int`):
            Width of patches to extract.
    """
    batch_size, channels, height, width = image_tensor.shape
    patches = torch.nn.functional.unfold(image_tensor, (patch_height, patch_width), stride=(patch_height, patch_width))
    patches = patches.reshape(batch_size, channels, patch_height, patch_width, -1)
    patches = patches.permute(0, 4, 2, 3, 1).reshape(
        batch_size, height // patch_height, width // patch_width, channels * patch_height * patch_width
    )
    return patches

