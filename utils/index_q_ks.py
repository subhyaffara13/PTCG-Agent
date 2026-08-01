
def index_QKs(alignment_heads: torch.Tensor, QKs: list[torch.Tensor]):  # noqa: N802
    """
    Compute the following to get stacked QK tensor that has been indexed for the desired attention heads:
    weights = torch.stack([QKs[_l][:, _h] for _l, _h in alignment_heads], dim=1)
    """
    indexed_QKs = []  # noqa: N806
    for pair in alignment_heads:
        # Each QK is of shape (batch_size, num_heads, sequence_length, num_frames // 2)
        # The `QKs[_l]` selects the right QK from the list of QKs
        # The `QKs[_l][:, _h]` selects the right attention heads from the chosen QK. The `:` is to do this for the batch dim.
        #
        # PyTorch:
        # QKs[_l] is of shape (batch_size, num_heads, sequence_length, num_frames // 2)
        # QKs[_l][:, _h] is of shape (batch_size, sequence_length, num_frames // 2)
        #
        # ONNX:
        # QKs[_l] is of shape (batch_size, num_heads, sequence_length, num_frames // 2)
        # QKs[_l][:, _h] is of shape (batch_size, 1, sequence_length, num_frames // 2) because
        # the `[:, _h]` operation maps to a Gather op and that op does not reduce dimensions
        _l, _h = pair[0], pair[1]
        indexed_QKs.append(QKs[_l][:, _h])

    # PyTorch:
    # torch.stack will return a tensor of shape (batch_size, num_alignment_heads, sequence_length, num_frames // 2).
    #
    # ONNX:
    # torch.stack will return a tensor of shape (batch_size, num_alignment_heads, 1, sequence_length, num_frames // 2)
    # because the Gather op does not reduce dimensions. To remove the unneeded dimension, torch.squeeze with a specified
    # dim (dim = 2) is added. The torch.squeeze op with a specified dim only runs if the specified dim has a size of 1.
    # Since the dim won't be of size 1 in the PyTorch tensor but it is of size 1 in the ONNX tensor, it will be a no-op
    # in PyTorch and an op in ONNX. Thus, the Squeeze op will only affect the ONNX model.
    weights = torch.stack(indexed_QKs, dim=1)
    weights = torch.squeeze(weights, dim=2)
    return weights

