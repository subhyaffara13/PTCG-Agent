
def convert_video_to_patches(video: "torch.Tensor", patch_size: int) -> "torch.Tensor":
    """
    Convert 4D tensor video of shape (num_frames, num_channels, height, width) into 3D tensor of patches of shape
    (num_frames, num_patches_height * num_patches_width, patch_size * patch_size * num_channels).
    """
    num_frames, num_channels, height, width = video.shape
    num_patches_height = height // patch_size
    num_patches_width = width // patch_size
    patched_video = video.reshape(
        num_frames, num_channels, num_patches_height, patch_size, num_patches_width, patch_size
    )
    patched_video = patched_video.permute(0, 2, 4, 3, 5, 1)
    patched_video = patched_video.reshape(num_frames, num_patches_height * num_patches_width, -1)
    return patched_video


def convert_video_to_patches(video: "torch.Tensor", patch_size: int) -> "torch.Tensor":
    """
    Convert 4D tensor video of shape (num_frames, num_channels, height, width) into 3D tensor of patches of shape
    (num_frames, num_patches_height * num_patches_width, patch_size * patch_size * num_channels).
    """
    num_frames, num_channels, height, width = video.shape
    num_patches_height = height // patch_size
    num_patches_width = width // patch_size
    patched_video = video.reshape(
        num_frames, num_channels, num_patches_height, patch_size, num_patches_width, patch_size
    )
    patched_video = patched_video.permute(0, 2, 4, 3, 5, 1)
    patched_video = patched_video.reshape(num_frames, num_patches_height * num_patches_width, -1)
    return patched_video

