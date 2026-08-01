
def get_lexer_for_filename(_fn, code=None, **options):
    """Get a lexer for a filename.

    Return a `Lexer` subclass instance that has a filename pattern
    matching `fn`. The lexer is given the `options` at its
    instantiation.

    Raise :exc:`pygments.util.ClassNotFound` if no lexer for that filename
    is found.

    If multiple lexers match the filename pattern, use their ``analyse_text()``
    methods to figure out which one is more appropriate.
    """
    res = find_lexer_class_for_filename(_fn, code)
    if not res:
        raise ClassNotFound(f'no lexer for filename {_fn!r} found')
    return res(**options)


def get_lexer_for_filename(_fn, code=None, **options):
    """Get a lexer for a filename.

    Return a `Lexer` subclass instance that has a filename pattern
    matching `fn`. The lexer is given the `options` at its
    instantiation.

    Raise :exc:`pygments.util.ClassNotFound` if no lexer for that filename
    is found.

    If multiple lexers match the filename pattern, use their ``analyse_text()``
    methods to figure out which one is more appropriate.
    """
    res = find_lexer_class_for_filename(_fn, code)
    if not res:
        raise ClassNotFound(f'no lexer for filename {_fn!r} found')
    return res(**options)

