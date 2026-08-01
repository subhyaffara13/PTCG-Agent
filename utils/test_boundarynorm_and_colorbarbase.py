
def test_boundarynorm_and_colorbarbase():
    # Make a figure and axes with dimensions as desired.
    fig = plt.figure()
    ax1 = fig.add_axes((0.05, 0.80, 0.9, 0.15))
    ax2 = fig.add_axes((0.05, 0.475, 0.9, 0.15))
    ax3 = fig.add_axes((0.05, 0.15, 0.9, 0.15))

    # Set the colormap and bounds
    bounds = [-1, 2, 5, 7, 12, 15]
    cmap = mpl.colormaps['viridis']

    # Default behavior
    norm = mcolors.BoundaryNorm(bounds, cmap.N)
    cb1 = mcolorbar.ColorbarBase(ax1, cmap=cmap, norm=norm, extend='both',
                                 orientation='horizontal', spacing='uniform')
    # New behavior
    norm = mcolors.BoundaryNorm(bounds, cmap.N, extend='both')
    cb2 = mcolorbar.ColorbarBase(ax2, cmap=cmap, norm=norm,
                                 orientation='horizontal')

    # User can still force to any extend='' if really needed
    norm = mcolors.BoundaryNorm(bounds, cmap.N, extend='both')
    cb3 = mcolorbar.ColorbarBase(ax3, cmap=cmap, norm=norm,
                                 extend='neither', orientation='horizontal')

