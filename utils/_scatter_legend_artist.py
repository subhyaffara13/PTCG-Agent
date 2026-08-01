
def _scatter_legend_artist(**kws):

    kws = normalize_kwargs(kws, mpl.collections.PathCollection)

    edgecolor = kws.pop("edgecolor", None)
    rc = mpl.rcParams
    line_kws = {
        "linestyle": "",
        "marker": kws.pop("marker", "o"),
        "markersize": np.sqrt(kws.pop("s", rc["lines.markersize"] ** 2)),
        "markerfacecolor": kws.pop("facecolor", kws.get("color")),
        "markeredgewidth": kws.pop("linewidth", 0),
        **kws,
    }

    if edgecolor is not None:
        if edgecolor == "face":
            line_kws["markeredgecolor"] = line_kws["markerfacecolor"]
        else:
            line_kws["markeredgecolor"] = edgecolor

    return mpl.lines.Line2D([], [], **line_kws)

