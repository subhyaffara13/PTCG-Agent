
def find_peaks_signature(
    x, height=None, threshold=None, distance=None, prominence=None, width=None,
    wlen=None, rel_height=0.5, plateau_size=None
):
    # TODO: fix me - `prominence` is not necessarily an array.
    # return array_namespace(x, height, threshold, prominence, width, plateau_size)
    # See https://github.com/scipy/scipy/pull/22644#issuecomment-3568443768. For now:
    return np_compat

