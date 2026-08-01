
def _correlation_cdist_wrap(XA, XB, dm, **kwargs):
    XA = XA - XA.mean(axis=1, keepdims=True)
    XB = XB - XB.mean(axis=1, keepdims=True)
    _distance_wrap.cdist_cosine_double_wrap(XA, XB, dm, **kwargs)

