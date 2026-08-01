
def _safe_norm(v):
    if not np.isfinite(v).all():
        return np.array(np.inf)
    return norm(v)

