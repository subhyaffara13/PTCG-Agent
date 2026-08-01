
def _compute_source_index(scale, dst_index, align_corners):
    if align_corners:
        return scale * dst_index
    else:
        return scale * (dst_index + 0.5) - 0.5

