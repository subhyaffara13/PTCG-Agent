
def _pad_along_last_axis(X, m, *, xp):
    """Pad the data for computing the rolling window difference."""
    # scales a  bit better than method in _vasicek_like_entropy
    shape = X.shape[:-1] + (m,)
    Xl = xp.broadcast_to(X[..., :1], shape)  # :1 vs 0 to maintain shape
    Xr = xp.broadcast_to(X[..., -1:], shape)
    return xp.concat((Xl, X, Xr), axis=-1)

