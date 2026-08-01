
def _cdist_callable(XA, XB, *, out, metric, **kwargs):
    mA = XA.shape[0]
    mB = XB.shape[0]
    dm = _prepare_out_argument(out, np.float64, (mA, mB))
    for i in range(mA):
        for j in range(mB):
            dm[i, j] = metric(XA[i], XB[j], **kwargs)
    return dm

