
def _remove_labels_from_axis(axis: Axis) -> None:
    for t in axis.get_majorticklabels():
        t.set_visible(False)

    # set_visible will not be effective if
    # minor axis has NullLocator and NullFormatter (default)
    if isinstance(axis.get_minor_locator(), mpl.ticker.NullLocator):
        axis.set_minor_locator(mpl.ticker.AutoLocator())
    if isinstance(axis.get_minor_formatter(), mpl.ticker.NullFormatter):
        axis.set_minor_formatter(mpl.ticker.FormatStrFormatter(""))
    for t in axis.get_minorticklabels():
        t.set_visible(False)

    axis.get_label().set_visible(False)

