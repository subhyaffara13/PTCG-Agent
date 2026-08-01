
def get_style_by_name(name):
    """
    Return a style class by its short name. The names of the builtin styles
    are listed in :data:`pygments.styles.STYLE_MAP`.

    Will raise :exc:`pygments.util.ClassNotFound` if no style of that name is
    found.
    """
    if name in _STYLE_NAME_TO_MODULE_MAP:
        mod, cls = _STYLE_NAME_TO_MODULE_MAP[name]
        builtin = "yes"
    else:
        for found_name, style in find_plugin_styles():
            if name == found_name:
                return style
        # perhaps it got dropped into our styles package
        builtin = ""
        mod = 'pygments.styles.' + name
        cls = name.title() + "Style"

    try:
        mod = __import__(mod, None, None, [cls])
    except ImportError:
        raise ClassNotFound(f"Could not find style module {mod!r}" +
                            (builtin and ", though it should be builtin")
                            + ".")
    try:
        return getattr(mod, cls)
    except AttributeError:
        raise ClassNotFound(f"Could not find style class {cls!r} in style module.")


def get_style_by_name(name):
    """
    Return a style class by its short name. The names of the builtin styles
    are listed in :data:`pygments.styles.STYLE_MAP`.

    Will raise :exc:`pygments.util.ClassNotFound` if no style of that name is
    found.
    """
    if name in _STYLE_NAME_TO_MODULE_MAP:
        mod, cls = _STYLE_NAME_TO_MODULE_MAP[name]
        builtin = "yes"
    else:
        for found_name, style in find_plugin_styles():
            if name == found_name:
                return style
        # perhaps it got dropped into our styles package
        builtin = ""
        mod = 'pygments.styles.' + name
        cls = name.title() + "Style"

    try:
        mod = __import__(mod, None, None, [cls])
    except ImportError:
        raise ClassNotFound(f"Could not find style module {mod!r}" +
                            (builtin and ", though it should be builtin")
                            + ".")
    try:
        return getattr(mod, cls)
    except AttributeError:
        raise ClassNotFound(f"Could not find style class {cls!r} in style module.")

