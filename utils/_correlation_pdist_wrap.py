
def _correlation_pdist_wrap(X, dm, **kwargs):
    X2 = X - X.mean(axis=1, keepdims=True)
    _distance_wrap.pdist_cosine_double_wrap(X2, dm, **kwargs)

