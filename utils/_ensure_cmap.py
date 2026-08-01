
def _ensure_cmap(cmap, accept_multivariate=False):
    """
    Ensure that we have a `.Colormap` object.

    For internal use to preserve type stability of errors.

    Parameters
    ----------
    cmap : None, str, Colormap

        - if a `~matplotlib.colors.Colormap`,
          `~matplotlib.colors.MultivarColormap` or
          `~matplotlib.colors.BivarColormap`,
          return it
        - if a string, look it up in three corresponding databases
          when not found: raise an error based on the expected shape
        - if None, look up the default color map in mpl.colormaps
    accept_multivariate : bool, default False
        - if False, accept only Colormap, string in mpl.colormaps or None

    Returns
    -------
    Colormap

    """
    if accept_multivariate:
        types = (colors.Colormap, colors.BivarColormap, colors.MultivarColormap)
        mappings = (mpl.colormaps, mpl.multivar_colormaps, mpl.bivar_colormaps)
    else:
        types = (colors.Colormap, )
        mappings = (mpl.colormaps, )

    if isinstance(cmap, types):
        return cmap

    cmap_name = mpl._val_or_rc(cmap, "image.cmap")

    for mapping in mappings:
        if cmap_name in mapping:
            return mapping[cmap_name]

    # this error message is a variant of _api.check_in_list but gives
    # additional hints as to how to access multivariate colormaps

    raise ValueError(_api.list_suggestion_error_msg('cmap', cmap, mpl.colormaps) +
                     "\nSee `matplotlib.bivar_colormaps()` and"
                     " `matplotlib.multivar_colormaps()` for"
                     " bivariate and multivariate colormaps")

