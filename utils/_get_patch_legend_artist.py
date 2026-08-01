
def _get_patch_legend_artist(fill):

    def legend_artist(**kws):

        color = kws.pop("color", None)
        if color is not None:
            if fill:
                kws["facecolor"] = color
            else:
                kws["edgecolor"] = color
                kws["facecolor"] = "none"

        return mpl.patches.Rectangle((0, 0), 0, 0, **kws)

    return legend_artist

