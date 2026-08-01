
def get_formatter_for_filename(fn, **options):
    """
    Return a :class:`.Formatter` subclass instance that has a filename pattern
    matching `fn`. The formatter is given the `options` at its instantiation.

    Will raise :exc:`pygments.util.ClassNotFound` if no formatter for that filename
    is found.
    """
    fn = basename(fn)
    for modname, name, _, filenames, _ in FORMATTERS.values():
        for filename in filenames:
            if _fn_matches(fn, filename):
                if name not in _formatter_cache:
                    _load_formatters(modname)
                return _formatter_cache[name](**options)
    for _name, cls in find_plugin_formatters():
        for filename in cls.filenames:
            if _fn_matches(fn, filename):
                return cls(**options)
    raise ClassNotFound(f"no formatter found for file name {fn!r}")


def get_formatter_for_filename(fn, **options):
    """
    Return a :class:`.Formatter` subclass instance that has a filename pattern
    matching `fn`. The formatter is given the `options` at its instantiation.

    Will raise :exc:`pygments.util.ClassNotFound` if no formatter for that filename
    is found.
    """
    fn = basename(fn)
    for modname, name, _, filenames, _ in FORMATTERS.values():
        for filename in filenames:
            if _fn_matches(fn, filename):
                if name not in _formatter_cache:
                    _load_formatters(modname)
                return _formatter_cache[name](**options)
    for _name, cls in find_plugin_formatters():
        for filename in cls.filenames:
            if _fn_matches(fn, filename):
                return cls(**options)
    raise ClassNotFound(f"no formatter found for file name {fn!r}")

