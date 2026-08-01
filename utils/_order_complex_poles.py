
def _order_complex_poles(poles):
    """
    Check we have complex conjugates pairs and reorder P according to YT, ie
    real_poles, complex_i, conjugate complex_i, ....
    The lexicographic sort on the complex poles is added to help the user to
    compare sets of poles.
    """
    ordered_poles = np.sort(poles[np.isreal(poles)])
    im_poles = []
    for p in np.sort(poles[np.imag(poles) < 0]):
        if np.conj(p) in poles:
            im_poles.extend((p, np.conj(p)))

    ordered_poles = np.hstack((ordered_poles, im_poles))

    if poles.shape[0] != len(ordered_poles):
        raise ValueError("Complex poles must come with their conjugates")
    return ordered_poles

