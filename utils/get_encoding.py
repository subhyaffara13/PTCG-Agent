
def get_encoding(encoding_name: str) -> Encoding:
    if not isinstance(encoding_name, str):
        raise ValueError(f"Expected a string in get_encoding, got {type(encoding_name)}")

    if encoding_name in ENCODINGS:
        return ENCODINGS[encoding_name]

    with _lock:
        if encoding_name in ENCODINGS:
            return ENCODINGS[encoding_name]

        if ENCODING_CONSTRUCTORS is None:
            _find_constructors()
            assert ENCODING_CONSTRUCTORS is not None

        if encoding_name not in ENCODING_CONSTRUCTORS:
            raise ValueError(
                f"Unknown encoding {encoding_name}.\n"
                f"Plugins found: {_available_plugin_modules()}\n"
                f"tiktoken version: {tiktoken.__version__} (are you on latest?)"
            )

        constructor = ENCODING_CONSTRUCTORS[encoding_name]
        enc = Encoding(**constructor())
        ENCODINGS[encoding_name] = enc
        return enc


def getEncoding(platformID, platEncID, langID, default=None):
    """Returns the Python encoding name for OpenType platformID/encodingID/langID
    triplet.  If encoding for these values is not known, by default None is
    returned.  That can be overriden by passing a value to the default argument.
    """
    encoding = _encodingMap.get(platformID, {}).get(platEncID, default)
    if isinstance(encoding, dict):
        encoding = encoding.get(langID, encoding[Ellipsis])
    return encoding

