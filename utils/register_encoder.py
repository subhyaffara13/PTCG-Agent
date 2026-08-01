
def register_encoder(name: str, encoder: type[ImageFile.PyEncoder]) -> None:
    """
    Registers an image encoder.  This function should not be
    used in application code.

    :param name: The name of the encoder
    :param encoder: An ImageFile.PyEncoder object

    .. versionadded:: 4.1.0
    """
    ENCODERS[name] = encoder


def register_encoder(encoder: E) -> E:
    """Add a custom encoder, which should be a function that will be called
    if the value can't otherwise be converted.

    The encoder should return a TOMLKit item or raise a ``ConvertError``.

    Example:
        @register_encoder
        def encode_custom_dict(obj, _parent=None, _sort_keys=False):
            if isinstance(obj, CustomDict):
                tbl = table()
                for key, value in obj.items():
                    # Pass along parameters when encoding nested values
                    tbl[key] = item(value, _parent=tbl, _sort_keys=_sort_keys)
                return tbl
            raise ConvertError("Not a CustomDict")
    """
    CUSTOM_ENCODERS.append(encoder)
    return encoder

