
def test_format_cursor_data_multinorm(data, text):
    from matplotlib.backend_bases import MouseEvent
    fig, ax = plt.subplots()
    cmap_bivar = mpl.bivar_colormaps['BiOrangeBlue']
    cmap_multivar = mpl.multivar_colormaps['2VarAddA']

    # This is a test for ColorizingArtist._format_cursor_data_override()
    # with data with multiple channels.
    # It includes a workaround so that we can test this functionality
    # before the MultiVar/BiVariate colormaps and MultiNorm are exposed
    # via the top-level methods (ax.imshow())
    # i.e. we here set the hidden variables _cmap and _norm
    # and use set_array() on the ColorizingArtist rather than the _ImageBase
    # but this workaround should be replaced by:
    #  `ax.imshow(data, cmap=cmap_bivar, vmin=(0,0), vmax=(1,1))`
    # once the functionality is available.
    # see https://github.com/matplotlib/matplotlib/issues/14168
    im = ax.imshow([[0, 1]])
    im.colorizer._cmap = cmap_bivar
    im.colorizer._norm = colors.MultiNorm([im.norm, im.norm])
    mpl.colorizer.ColorizingArtist.set_array(im, data)

    xdisp, ydisp = ax.transData.transform([0, 0])
    event = MouseEvent('motion_notify_event', fig.canvas, xdisp, ydisp)
    assert im.format_cursor_data(im.get_cursor_data(event)) == text

    im.colorizer._cmap = cmap_multivar
    event = MouseEvent('motion_notify_event', fig.canvas, xdisp, ydisp)
    assert im.format_cursor_data(im.get_cursor_data(event)) == text

