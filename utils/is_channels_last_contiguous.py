
def is_channels_last_contiguous(a: Tensor) -> bool:
    """
    True when a tensor is channels-last contiguous.

    This requires that:

      - the tensor is conceptually either 4 (NHWC) or 5 (NDHWC) dimensions
      - if we name the tensor's dimensions NCHW or NCDHW, then the strides are such that the
        stride of the 'C' dimension (Cs) is 1 and the strides corresponding to
        each dimension (Xs) can be ordered Cs <= Ws <= Hs <= (Ds) <= Ns and are
        "nested" -- so Ws = Cs * Cl, where Cl is the length of the 'C' dimension,
        for example.
    """
    return is_channels_last_contiguous_2d(a) or is_channels_last_contiguous_3d(a)

