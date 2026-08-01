
def get_colormap(name):
    """Handle changes to matplotlib colormap interface in 3.6."""
    try:
        return mpl.colormaps[name]
    except AttributeError:
        return mpl.cm.get_cmap(name)

