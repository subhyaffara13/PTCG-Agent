
def boards_to_ndarray(boards):
    arr64 = np.array(boards, dtype=np.uint64)
    arr8 = arr64.view(dtype=np.uint8)
    # a bit array increment from LHS to RHS
    bits = np.unpackbits(arr8, bitorder="little")
    floats = bits.astype(bool)
    boardstack = floats.reshape([len(boards), 8, 8])
    # We do np.flip() onto `boardstack` because the 1st line of the boardimage is the 8th line of the ndarray.
    boardimage = np.flip(np.transpose(boardstack, [1, 2, 0]), axis=0)
    return boardimage

