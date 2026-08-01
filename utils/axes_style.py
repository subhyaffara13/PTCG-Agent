
def axes_style(style=None, rc=None):
    """
    Get the parameters that control the general style of the plots.

    The style parameters control properties like the color of the background and
    whether a grid is enabled by default. This is accomplished using the
    matplotlib rcParams system.

    The options are illustrated in the
    :doc:`aesthetics tutorial <../tutorial/aesthetics>`.

    This function can also be used as a context manager to temporarily
    alter the global defaults. See :func:`set_theme` or :func:`set_style`
    to modify the global defaults for all plots.

    Parameters
    ----------
    style : None, dict, or one of {darkgrid, whitegrid, dark, white, ticks}
        A dictionary of parameters or the name of a preconfigured style.
    rc : dict, optional
        Parameter mappings to override the values in the preset seaborn
        style dictionaries. This only updates parameters that are
        considered part of the style definition.

    Examples
    --------

    .. include:: ../docstrings/axes_style.rst

    """
    if style is None:
        style_dict = {k: mpl.rcParams[k] for k in _style_keys}

    elif isinstance(style, dict):
        style_dict = style

    else:
        styles = ["white", "dark", "whitegrid", "darkgrid", "ticks"]
        if style not in styles:
            raise ValueError(f"style must be one of {', '.join(styles)}")

        # Define colors here
        dark_gray = ".15"
        light_gray = ".8"

        # Common parameters
        style_dict = {

            "figure.facecolor": "white",
            "axes.labelcolor": dark_gray,

            "xtick.direction": "out",
            "ytick.direction": "out",
            "xtick.color": dark_gray,
            "ytick.color": dark_gray,

            "axes.axisbelow": True,
            "grid.linestyle": "-",


            "text.color": dark_gray,
            "font.family": ["sans-serif"],
            "font.sans-serif": ["Arial", "DejaVu Sans", "Liberation Sans",
                                "Bitstream Vera Sans", "sans-serif"],


            "lines.solid_capstyle": "round",
            "patch.edgecolor": "w",
            "patch.force_edgecolor": True,

            "image.cmap": "rocket",

            "xtick.top": False,
            "ytick.right": False,

        }

        # Set grid on or off
        if "grid" in style:
            style_dict.update({
                "axes.grid": True,
            })
        else:
            style_dict.update({
                "axes.grid": False,
            })

        # Set the color of the background, spines, and grids
        if style.startswith("dark"):
            style_dict.update({

                "axes.facecolor": "#EAEAF2",
                "axes.edgecolor": "white",
                "grid.color": "white",

                "axes.spines.left": True,
                "axes.spines.bottom": True,
                "axes.spines.right": True,
                "axes.spines.top": True,

            })

        elif style == "whitegrid":
            style_dict.update({

                "axes.facecolor": "white",
                "axes.edgecolor": light_gray,
                "grid.color": light_gray,

                "axes.spines.left": True,
                "axes.spines.bottom": True,
                "axes.spines.right": True,
                "axes.spines.top": True,

            })

        elif style in ["white", "ticks"]:
            style_dict.update({

                "axes.facecolor": "white",
                "axes.edgecolor": dark_gray,
                "grid.color": light_gray,

                "axes.spines.left": True,
                "axes.spines.bottom": True,
                "axes.spines.right": True,
                "axes.spines.top": True,

            })

        # Show or hide the axes ticks
        if style == "ticks":
            style_dict.update({
                "xtick.bottom": True,
                "ytick.left": True,
            })
        else:
            style_dict.update({
                "xtick.bottom": False,
                "ytick.left": False,
            })

    # Remove entries that are not defined in the base list of valid keys
    # This lets us handle matplotlib <=/> 2.0
    style_dict = {k: v for k, v in style_dict.items() if k in _style_keys}

    # Override these settings with the provided rc dictionary
    if rc is not None:
        rc = {k: v for k, v in rc.items() if k in _style_keys}
        style_dict.update(rc)

    # Wrap in an _AxesStyle object so this can be used in a with statement
    style_object = _AxesStyle(style_dict)

    return style_object

