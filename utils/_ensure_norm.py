
def _ensure_norm(norm, n_components=1):
    if n_components == 1:
        _api.check_isinstance((colors.Norm, str, None), norm=norm)
        if norm is None:
            norm = colors.Normalize()
        elif isinstance(norm, str):
            scale_cls = _api.getitem_checked(scale._scale_mapping, norm=norm)
            return _auto_norm_from_scale(scale_cls)()
        return norm
    elif n_components > 1:
        if not np.iterable(norm):
            _api.check_isinstance((colors.MultiNorm, None, tuple), norm=norm)
        if norm is None:
            norm = colors.MultiNorm(['linear']*n_components)
        else:  # iterable, i.e. multiple strings or Normalize objects
            norm = colors.MultiNorm(norm)
        if isinstance(norm, colors.MultiNorm) and norm.n_components == n_components:
            return norm
        raise ValueError(
            f"Invalid norm for multivariate colormap with {n_components} inputs")
    else:  # n_components == 0
        raise ValueError(
            "Invalid cmap. A colorizer object must have a cmap with `n_variates` >= 1")

