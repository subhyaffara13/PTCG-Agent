
def search_function(name: str) -> Optional[codecs.CodecInfo]:
    """Codec search function registered with :mod:`codecs`.

    Returns a :class:`codecs.CodecInfo` for the ``"idna2008"`` codec name
    so that ``str.encode("idna2008")`` and ``bytes.decode("idna2008")``
    invoke the IDNA 2008 codec defined in this module.

    :param name: The codec name being looked up.
    :returns: A :class:`codecs.CodecInfo` instance if ``name`` is
        ``"idna2008"``, otherwise ``None``.
    """
    if name != "idna2008":
        return None
    return codecs.CodecInfo(
        name=name,
        encode=Codec().encode,
        decode=Codec().decode,  # type: ignore
        incrementalencoder=IncrementalEncoder,
        incrementaldecoder=IncrementalDecoder,
        streamwriter=StreamWriter,
        streamreader=StreamReader,
    )


def search_function(name: str) -> Optional[codecs.CodecInfo]:
    if name != "idna2008":
        return None
    return codecs.CodecInfo(
        name=name,
        encode=Codec().encode,
        decode=Codec().decode,  # type: ignore
        incrementalencoder=IncrementalEncoder,
        incrementaldecoder=IncrementalDecoder,
        streamwriter=StreamWriter,
        streamreader=StreamReader,
    )


def search_function(name):
    name = encodings.normalize_encoding(name)  # Rather undocumented...
    if name in _extended_encodings:
        if name not in _cache:
            base_encoding, mapping = _extended_encodings[name]
            assert name[-4:] == "_ttx"
            # Python 2 didn't have any of the encodings that we are implementing
            # in this file.  Python 3 added aliases for the East Asian ones, mapping
            # them "temporarily" to the same base encoding as us, with a comment
            # suggesting that full implementation will appear some time later.
            # As such, try the Python version of the x_mac_... first, if that is found,
            # use *that* as our base encoding.  This would make our encoding upgrade
            # to the full encoding when and if Python finally implements that.
            # http://bugs.python.org/issue24041
            base_encodings = [name[:-4], base_encoding]
            for base_encoding in base_encodings:
                try:
                    codecs.lookup(base_encoding)
                except LookupError:
                    continue
                _cache[name] = ExtendCodec(name, base_encoding, mapping)
                break
        return _cache[name].info

    return None

