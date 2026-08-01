
def py_encode_basestring(s, _PY3=PY3, _q=u'"'):
    """Return a JSON representation of a Python string

    """
    if _PY3:
        if isinstance(s, bytes):
            s = str(s, 'utf-8')
        elif type(s) is not str:
            # convert an str subclass instance to exact str
            # raise a TypeError otherwise
            s = str.__str__(s)
    else:
        if isinstance(s, str) and HAS_UTF8.search(s) is not None:
            s = unicode(s, 'utf-8')
        elif type(s) not in (str, unicode):
            # convert an str subclass instance to exact str
            # convert a unicode subclass instance to exact unicode
            # raise a TypeError otherwise
            if isinstance(s, str):
                s = str.__str__(s)
            else:
                s = unicode.__getnewargs__(s)[0]
    def replace(match):
        return ESCAPE_DCT[match.group(0)]
    return _q + ESCAPE.sub(replace, s) + _q

