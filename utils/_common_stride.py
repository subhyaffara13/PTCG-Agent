
def _common_stride(offsets, counts, itemsize):
    """
    Returns the stride between the fields, or None if the stride is not
    constant. The values in "counts" designate the lengths of
    subarrays. Subarrays are treated as many contiguous fields, with
    always positive stride.
    """
    if len(offsets) <= 1:
        return itemsize

    negative = offsets[1] < offsets[0]  # negative stride
    if negative:
        # reverse, so offsets will be ascending
        it = zip(reversed(offsets), reversed(counts))
    else:
        it = zip(offsets, counts)

    prev_offset = None
    stride = None
    for offset, count in it:
        if count != 1:  # subarray: always c-contiguous
            if negative:
                return None  # subarrays can never have a negative stride
            if stride is None:
                stride = itemsize
            if stride != itemsize:
                return None
            end_offset = offset + (count - 1) * itemsize
        else:
            end_offset = offset

        if prev_offset is not None:
            new_stride = offset - prev_offset
            if stride is None:
                stride = new_stride
            if stride != new_stride:
                return None

        prev_offset = end_offset

    if negative:
        return -stride
    return stride

