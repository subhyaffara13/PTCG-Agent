
def rescale_stride(stride, ratio):
    """
    Rescales the stride values from audio space to tokens/logits space.

    (160_000, 16_000, 16_000) -> (2000, 200, 200) for instance.
    """
    # Shape is [B, SEQ] for tokens
    # [B, SEQ, V] for logits

    new_strides = []
    for input_n, left, right in stride:
        token_n = int(round(input_n * ratio))
        left = int(round(left / input_n * token_n))
        right = int(round(right / input_n * token_n))
        new_stride = (token_n, left, right)
        new_strides.append(new_stride)

    return new_strides

