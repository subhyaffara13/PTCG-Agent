
def _get_feat_extract_output_lengths(input_lengths):
    """Compute output lengths after the 3-layer CNN feature extractor with deepstack.

    Three stride-2 convolutions within each 100-frame block, plus 13 output frames
    per full block from the deepstack path.
    """
    input_lengths_leave = input_lengths % 100
    feat_lengths = (input_lengths_leave - 1) // 2 + 1
    return ((feat_lengths - 1) // 2 + 1 - 1) // 2 + 1 + (input_lengths // 100) * 13


def _get_feat_extract_output_lengths(input_lengths):
    """Compute output lengths after the 3-layer CNN feature extractor with deepstack.

    Three stride-2 convolutions within each 100-frame block, plus 13 output frames
    per full block from the deepstack path.
    """
    input_lengths_leave = input_lengths % 100
    feat_lengths = (input_lengths_leave - 1) // 2 + 1
    return ((feat_lengths - 1) // 2 + 1 - 1) // 2 + 1 + (input_lengths // 100) * 13


def _get_feat_extract_output_lengths(input_lengths):
    """Compute output lengths after the 3-layer CNN feature extractor with deepstack.

    Three stride-2 convolutions within each 100-frame block, plus 13 output frames
    per full block from the deepstack path.
    """
    input_lengths_leave = input_lengths % 100
    feat_lengths = (input_lengths_leave - 1) // 2 + 1
    return ((feat_lengths - 1) // 2 + 1 - 1) // 2 + 1 + (input_lengths // 100) * 13

