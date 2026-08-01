
def _show_cmap(cmap):
    """Show a continuous matplotlib colormap."""
    from .rcmod import axes_style  # Avoid circular import
    with axes_style("white"):
        f, ax = plt.subplots(figsize=(8.25, .75))
    ax.set(xticks=[], yticks=[])
    x = np.linspace(0, 1, 256)[np.newaxis, :]
    ax.pcolormesh(x, cmap=cmap)

