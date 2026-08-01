
def get_lexer_for_mimetype(_mime, **options):
    """
    Return a `Lexer` subclass instance that has `mime` in its mimetype
    list. The lexer is given the `options` at its instantiation.

    Will raise :exc:`pygments.util.ClassNotFound` if not lexer for that mimetype
    is found.
    """
    for modname, name, _, _, mimetypes in LEXERS.values():
        if _mime in mimetypes:
            if name not in _lexer_cache:
                _load_lexers(modname)
            return _lexer_cache[name](**options)
    for cls in find_plugin_lexers():
        if _mime in cls.mimetypes:
            return cls(**options)
    raise ClassNotFound(f'no lexer for mimetype {_mime!r} found')


def get_lexer_for_mimetype(_mime, **options):
    """
    Return a `Lexer` subclass instance that has `mime` in its mimetype
    list. The lexer is given the `options` at its instantiation.

    Will raise :exc:`pygments.util.ClassNotFound` if not lexer for that mimetype
    is found.
    """
    for modname, name, _, _, mimetypes in LEXERS.values():
        if _mime in mimetypes:
            if name not in _lexer_cache:
                _load_lexers(modname)
            return _lexer_cache[name](**options)
    for cls in find_plugin_lexers():
        if _mime in cls.mimetypes:
            return cls(**options)
    raise ClassNotFound(f'no lexer for mimetype {_mime!r} found')

