
def _lin_est(data):
    # Eh. The answer is analytical, so just return all ones.
    # Don't return zeros since that will interfere with
    # ODRPACK's auto-scaling procedures.

    if len(data.x.shape) == 2:
        m = data.x.shape[0]
    else:
        m = 1

    return np.ones((m + 1,), float)

