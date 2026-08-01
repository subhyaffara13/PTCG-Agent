
def restructure(modality_sizes: ModalitySizeType, inputs: torch.Tensor) -> Mapping[str, torch.Tensor]:
    """
    Partitions a [B, N, C] tensor into tensors for each modality.

    Args:
        modality_sizes
            dict specifying the size of the modality
        inputs:
            input tensor

    Returns:
        dict mapping name of modality to its associated tensor.
    """
    outputs = {}
    index = 0
    # Apply a predictable ordering to the modalities
    for modality in sorted(modality_sizes.keys()):
        size = modality_sizes[modality]
        inp = inputs[:, index : index + size]
        index += size
        outputs[modality] = inp
    return outputs

