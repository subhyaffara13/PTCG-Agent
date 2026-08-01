
def xp_isscalar(x):
    return np.isscalar(x) or (is_array_api_obj(x) and x.ndim == 0)

