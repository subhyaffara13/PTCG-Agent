
def convert_image_to_patches(image: "torch.Tensor", patch_size: int) -> "torch.Tensor":
    """
    Convert 3D tensor image of shape (num_channels, image_height, image_width) into 2D tensor of patches of shape
    (num_patches_height * num_patches_width, patch_size * patch_size * num_channels).
    """
    num_channels, image_height, image_width = image.shape
    num_patches_height = image_height // patch_size
    num_patches_width = image_width // patch_size
    patched_image = image.reshape(num_channels, num_patches_height, patch_size, num_patches_width, patch_size)
    patched_image = patched_image.permute(1, 3, 2, 4, 0)
    patched_image = patched_image.reshape(num_patches_height * num_patches_width, -1)
    return patched_image


def convert_image_to_patches(image: np.ndarray, patch_size: int) -> np.ndarray:
    """
    Convert 3D array image of shape (num_channels, image_height, image_width) into 2D array of patches of shape
    (num_patches_height * num_patches_width, patch_size * patch_size * num_channels).
    """
    num_channels, image_height, image_width = image.shape
    num_patches_height = image_height // patch_size
    num_patches_width = image_width // patch_size
    patched_image = image.reshape(num_channels, num_patches_height, patch_size, num_patches_width, patch_size)
    patched_image = patched_image.transpose(1, 3, 2, 4, 0)
    patched_image = patched_image.reshape(num_patches_height * num_patches_width, -1)
    return patched_image


def convert_image_to_patches(image: "torch.Tensor", patch_size: int) -> "torch.Tensor":
    """
    Convert 3D tensor image of shape (num_channels, image_height, image_width) into 2D tensor of patches of shape
    (num_patches_height * num_patches_width, patch_size * patch_size * num_channels).
    """
    num_channels, image_height, image_width = image.shape
    num_patches_height = image_height // patch_size
    num_patches_width = image_width // patch_size
    patched_image = image.reshape(num_channels, num_patches_height, patch_size, num_patches_width, patch_size)
    patched_image = patched_image.permute(1, 3, 2, 4, 0)
    patched_image = patched_image.reshape(num_patches_height * num_patches_width, -1)
    return patched_image


def convert_image_to_patches(images: "torch.Tensor", patch_size: int) -> "torch.Tensor":
    """
    Convert 3D array image of shape (image_height, image_width, num_channels) into 2D array of patches of shape
    (num_patches_height * num_patches_width, patch_size * patch_size * num_channels).
    """
    batch_size, num_channels, image_height, image_width = images.shape
    num_patches_height = image_height // patch_size
    num_patches_width = image_width // patch_size
    patched_image = images.reshape(
        batch_size, num_channels, num_patches_height, patch_size, num_patches_width, patch_size
    )
    patched_image = patched_image.permute(0, 2, 4, 3, 5, 1)
    patched_image = patched_image.reshape(batch_size, num_patches_height * num_patches_width, -1)
    return patched_image


def convert_image_to_patches(image: np.ndarray, patch_size: int) -> np.ndarray:
    """
    Convert 3D array image of shape (num_channels, image_height, image_width) into 2D array of patches of shape
    (num_patches_height * num_patches_width, patch_size * patch_size * num_channels).
    """
    num_channels, image_height, image_width = image.shape
    num_patches_height = image_height // patch_size
    num_patches_width = image_width // patch_size
    patched_image = image.reshape(num_channels, num_patches_height, patch_size, num_patches_width, patch_size)
    patched_image = patched_image.transpose(1, 3, 2, 4, 0)
    patched_image = patched_image.reshape(num_patches_height * num_patches_width, -1)
    return patched_image


def convert_image_to_patches(image: "torch.Tensor", patch_size: int) -> "torch.Tensor":
    """
    Convert 3D tensor image of shape (num_channels, image_height, image_width) into 2D tensor of patches of shape
    (num_patches_height * num_patches_width, patch_size * patch_size * num_channels).
    """
    num_channels, image_height, image_width = image.shape
    num_patches_height = image_height // patch_size
    num_patches_width = image_width // patch_size
    patched_image = image.reshape(num_channels, num_patches_height, patch_size, num_patches_width, patch_size)
    patched_image = patched_image.permute(1, 3, 2, 4, 0)
    patched_image = patched_image.reshape(num_patches_height * num_patches_width, -1)
    return patched_image

