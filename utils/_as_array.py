
def _as_array(mgr):
    if mgr.ndim == 1:
        return mgr.external_values()
    return mgr.as_array().T

