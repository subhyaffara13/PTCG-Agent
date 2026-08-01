
def partial_ld_offset():
    return (
        12
        + 4 * (np.dtype("uint64").alignment > 4)
        + 8
        + 8 * (np.dtype("longdouble").alignment > 8)
    )

