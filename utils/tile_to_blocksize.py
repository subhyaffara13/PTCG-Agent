
def tile_to_blocksize(t, blocksize):
    *rest, m, n = t.shape
    new_shape = rest + [
        m // blocksize[0],
        blocksize[0],
        n // blocksize[1],
        blocksize[1],
    ]
    # using .view instead of .reshape to ensure that the result is
    # indeed a view:
    return t.view(new_shape).transpose(-3, -2)

