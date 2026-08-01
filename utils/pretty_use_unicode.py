
def pretty_use_unicode(flag=None):
    """Set whether pretty-printer should use unicode by default"""
    global _use_unicode, unicode_warnings
    if flag is None:
        return _use_unicode

    if flag and unicode_warnings:
        # print warnings (if any) on first unicode usage
        warnings.warn(unicode_warnings)
        unicode_warnings = ''

    use_unicode_prev = _use_unicode
    _use_unicode = flag
    return use_unicode_prev

