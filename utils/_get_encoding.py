
def _get_encoding():
    """Get encoding, loading it lazily if needed."""
    global _encoding_cache
    if _encoding_cache is None:
        import sys

        # Access via module to trigger __getattr__ if not cached
        _encoding_cache = sys.modules[__name__].encoding
    return _encoding_cache


def _get_encoding(encoding_or_label):
    """
    Accept either an encoding object or label.

    :param encoding: An :class:`Encoding` object or a label string.
    :returns: An :class:`Encoding` object.
    :raises: :exc:`~exceptions.LookupError` for an unknown label.

    """
    if hasattr(encoding_or_label, 'codec_info'):
        return encoding_or_label

    encoding = lookup(encoding_or_label)
    if encoding is None:
        raise LookupError('Unknown encoding label: %r' % encoding_or_label)
    return encoding

