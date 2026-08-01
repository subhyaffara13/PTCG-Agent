
def _default_color(method, hue, color, kws, saturation=1):
    """If needed, get a default color by using the matplotlib property cycle."""

    if hue is not None:
        # This warning is probably user-friendly, but it's currently triggered
        # in a FacetGrid context and I don't want to mess with that logic right now
        #  if color is not None:
        #      msg = "`color` is ignored when `hue` is assigned."
        #      warnings.warn(msg)
        return None

    kws = kws.copy()
    kws.pop("label", None)

    if color is not None:
        if saturation < 1:
            color = desaturate(color, saturation)
        return color

    elif method.__name__ == "plot":

        color = normalize_kwargs(kws, mpl.lines.Line2D).get("color")
        scout, = method([], [], scalex=False, scaley=False, color=color)
        color = scout.get_color()
        scout.remove()

    elif method.__name__ == "scatter":

        # Matplotlib will raise if the size of x/y don't match s/c,
        # and the latter might be in the kws dict
        scout_size = max(
            np.atleast_1d(kws.get(key, [])).shape[0]
            for key in ["s", "c", "fc", "facecolor", "facecolors"]
        )
        scout_x = scout_y = np.full(scout_size, np.nan)

        scout = method(scout_x, scout_y, **kws)
        facecolors = scout.get_facecolors()

        if not len(facecolors):
            # Handle bug in matplotlib <= 3.2 (I think)
            # This will limit the ability to use non color= kwargs to specify
            # a color in versions of matplotlib with the bug, but trying to
            # work out what the user wanted by re-implementing the broken logic
            # of inspecting the kwargs is probably too brittle.
            single_color = False
        else:
            single_color = np.unique(facecolors, axis=0).shape[0] == 1

        # Allow the user to specify an array of colors through various kwargs
        if "c" not in kws and single_color:
            color = to_rgb(facecolors[0])

        scout.remove()

    elif method.__name__ == "bar":

        # bar() needs masked, not empty data, to generate a patch
        scout, = method([np.nan], [np.nan], **kws)
        color = to_rgb(scout.get_facecolor())
        scout.remove()
        # Axes.bar adds both a patch and a container
        method.__self__.containers.pop(-1)

    elif method.__name__ == "fill_between":

        kws = normalize_kwargs(kws, mpl.collections.PolyCollection)
        scout = method([], [], **kws)
        facecolor = scout.get_facecolor()
        color = to_rgb(facecolor[0])
        scout.remove()

    if saturation < 1:
        color = desaturate(color, saturation)

    return color

