
def to_bytes(target) -> bytes:
  """Save optimizer or other object as msgpack-serialized state-dict.

  Args:
    target: template object with state-dict registrations to be
      serialized to msgpack format.  Typically a flax model or optimizer.

  Returns:
    Bytes of msgpack-encoded state-dict of ``target`` object.
  """
  state_dict = to_state_dict(target)
  return msgpack_serialize(state_dict, in_place=True)


def to_bytes(value: str | bytes, encoding: str = "utf-8") -> bytes:
    return value.encode(encoding) if isinstance(value, str) else value


def to_bytes(
    x: str | bytes, encoding: str | None = None, errors: str | None = None
) -> bytes:
    if isinstance(x, bytes):
        return x
    elif not isinstance(x, str):
        raise TypeError(f"not expecting type {type(x).__name__}")
    if encoding or errors:
        return x.encode(encoding or "utf-8", errors=errors or "strict")
    return x.encode()


def to_bytes(value, signed=False, length=0):
    length = max(value.bit_length(), length)

    if signed and length % 8 == 0:
        length += 1

    return value.to_bytes(length // 8 + (length % 8 and 1 or 0), 'big', signed=signed)


def to_bytes(
    x: str | bytes, encoding: str | None = None, errors: str | None = None
) -> bytes:
    if isinstance(x, bytes):
        return x
    elif not isinstance(x, str):
        raise TypeError(f"not expecting type {type(x).__name__}")
    if encoding or errors:
        return x.encode(encoding or "utf-8", errors=errors or "strict")
    return x.encode()


def to_bytes(value, encoding="utf-8"):
    """Converts a string value to bytes, if necessary.

    Args:
        value (Union[str, bytes]): The value to be converted.
        encoding (str): The encoding to use to convert unicode to bytes.
            Defaults to "utf-8".

    Returns:
        bytes: The original value converted to bytes (if unicode) or as
            passed in if it started out as bytes.

    Raises:
        google.auth.exceptions.InvalidValue: If the value could not be converted to bytes.
    """
    result = value.encode(encoding) if isinstance(value, str) else value
    if isinstance(result, bytes):
        return result
    else:
        raise exceptions.InvalidValue(
            "{0!r} could not be converted to bytes".format(value)
        )


def to_bytes(url):
    """to_bytes(u"URL") --> 'URL'."""
    # Most URL schemes require ASCII. If that changes, the conversion
    # can be relaxed.
    # XXX get rid of to_bytes()
    if isinstance(url, str):
        try:
            url = url.encode("ASCII").decode()
        except UnicodeError:
            raise UnicodeError("URL " + repr(url) +
                               " contains non-ASCII characters")
    return url

