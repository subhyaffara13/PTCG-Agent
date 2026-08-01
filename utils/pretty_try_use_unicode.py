
def pretty_try_use_unicode():
    """See if unicode output is available and leverage it if possible"""

    encoding = getattr(sys.stdout, 'encoding', None)

    # this happens when e.g. stdout is redirected through a pipe, or is
    # e.g. a cStringIO.StringO
    if encoding is None:
        return  # sys.stdout has no encoding

    symbols = []

    # see if we can represent greek alphabet
    symbols += greek_unicode.values()

    # and atoms
    symbols += atoms_table.values()

    for s in symbols:
        if s is None:
            return  # common symbols not present!

        try:
            s.encode(encoding)
        except UnicodeEncodeError:
            return

    # all the characters were present and encodable
    pretty_use_unicode(True)

