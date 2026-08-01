
def _calculate_scale(head_dim_size: int, scale: float | None) -> float:
    """
    For FlashAttention we pad the head dimension to be a multiple of 8 so we need to scale the output
    by the original head size and not the padded.
    """
    if scale is not None:
        return scale
    return 1.0 / math.sqrt(head_dim_size)


def _calculate_scale(query, scale):
    # TODO: Investigate why math.sqrt() isn't properly handled by Dynamo?
    softmax_scale = scale if scale is not None else torch.sym_sqrt(1.0 / query.size(-1))
    return softmax_scale

