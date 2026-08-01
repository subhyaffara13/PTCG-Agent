
def reconstruct_feature_maps(
    hidden_state: torch.Tensor, batch_size: int, padding: int, output_size: tuple[float, float]
) -> torch.Tensor:
    """
    Reconstructs feature maps from the hidden state produced by any of the encoder. Converts the hidden state of shape
    `(n_patches_per_batch * batch_size, seq_len, hidden_size)` to feature maps of shape
    `(batch_size, hidden_size, output_size[0], output_size[1])`.

    Args:
        hidden_state (torch.Tensor): Input tensor of shape `(n_patches_per_batch * batch_size, seq_len, hidden_size)`
            representing the encoded patches.
        batch_size (int): The number of samples in a batch.
        padding (int): The amount of padding to be removed when merging patches.
        output_size (tuple[float, float]): The desired output size for the feature maps, specified as `(height, width)`.

    Returns:
        torch.Tensor: Reconstructed feature maps of shape `(batch_size, hidden_size, output_size[0], output_size[1])`.
    """
    # reshape back to image like
    features = reshape_features(hidden_state)

    # merge all patches in a batch to create one large patch per batch
    features = merge_patches(
        features,
        batch_size=batch_size,
        padding=padding,
    )

    # interpolate patches to base size
    features = F.interpolate(
        features,
        size=output_size,
        mode="bilinear",
        align_corners=False,
    )

    return features

