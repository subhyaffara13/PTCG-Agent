
def test_iter_writemasked_broadcast_error(mask, mask_axes):
    # This assumes that a readwrite mask makes sense. This is likely not the
    # case and should simply be deprecated.
    arr = np.zeros((3, 4))
    itflags = ["reduce_ok"]
    mask_flags = ["arraymask", "readwrite", "allocate"]
    a_flags = ["writeonly", "writemasked"]
    if mask_axes is None:
        op_axes = None
    else:
        op_axes = [mask_axes, [0, 1]]

    with assert_raises(ValueError):
        np.nditer((mask, arr), flags=itflags, op_flags=[mask_flags, a_flags],
                  op_axes=op_axes)

