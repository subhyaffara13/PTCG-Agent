
def encode(
    s: Union[str, bytes, bytearray],
    strict: bool = False,
    uts46: bool = False,
    std3_rules: bool = False,
    transitional: bool = False,
) -> bytes:
    """Encode a Unicode domain name into its ASCII (A-label) form.

    Splits the input on label separators (only ``U+002E`` if ``strict`` is
    set; otherwise also IDEOGRAPHIC FULL STOP ``U+3002``, FULLWIDTH FULL
    STOP ``U+FF0E``, and HALFWIDTH IDEOGRAPHIC FULL STOP ``U+FF61``),
    encodes each label with :func:`alabel`, and rejoins them with ``.``.
    Optionally pre-processes the input through :func:`uts46_remap`.

    :param s: The domain name to encode.
    :param strict: If ``True``, only ``U+002E`` is recognised as a label
        separator.
    :param uts46: If ``True``, apply UTS #46 mapping before encoding.
    :param std3_rules: Forwarded to :func:`uts46_remap` when ``uts46`` is
        ``True``.
    :param transitional: Forwarded to :func:`uts46_remap` when ``uts46``
        is ``True``. Deprecated: emits a :class:`DeprecationWarning` and
        will be removed in a future version.
    :returns: The encoded domain as ASCII :class:`bytes`.
    :raises IDNAError: If the domain is empty, contains an invalid label,
        or exceeds the maximum domain length.
    """
    if transitional:
        warnings.warn(
            "Transitional processing has been removed from UTS #46. "
            "The transitional argument will be removed in a future version.",
            DeprecationWarning,
            stacklevel=2,
        )
    if not isinstance(s, str):
        try:
            s = str(s, "ascii")
        except (UnicodeDecodeError, TypeError) as err:
            raise IDNAError("should pass a unicode string to the function rather than a byte string.") from err
    if len(s) > _max_input_length:
        raise IDNAError("Domain too long")
    if uts46:
        s = uts46_remap(s, std3_rules, transitional)

    # Reject inputs that exceed the maximum DNS domain length up-front
    # to avoid expensive computation on long inputs.
    if not valid_string_length(s, trailing_dot=True):
        raise IDNAError("Domain too long")

    trailing_dot = False
    result = []
    labels = s.split(".") if strict else _unicode_dots_re.split(s)
    if not labels or labels == [""]:
        raise IDNAError("Empty domain")
    if labels[-1] == "":
        del labels[-1]
        trailing_dot = True
    for label in labels:
        s = alabel(label)
        if s:
            result.append(s)
        else:
            raise IDNAError("Empty label")
    if trailing_dot:
        result.append(b"")
    s = b".".join(result)
    if not valid_string_length(s, trailing_dot):
        raise IDNAError("Domain too long")
    return s


def encode(model="", text="", custom_tokenizer: Optional[dict] = None):
    """
    Encodes the given text using the specified model.

    Args:
        model (str): The name of the model to use for tokenization.
        custom_tokenizer (Optional[dict]): A custom tokenizer created with the `create_pretrained_tokenizer` or `create_tokenizer` method. Must be a dictionary with a string value for `type` and Tokenizer for `tokenizer`. Default is None.
        text (str): The text to be encoded.

    Returns:
        enc: The encoded text.
    """
    tokenizer_json = custom_tokenizer or _select_tokenizer(model=model)
    if isinstance(tokenizer_json["tokenizer"], Encoding):
        enc = tokenizer_json["tokenizer"].encode(text, disallowed_special=())
    else:
        enc = tokenizer_json["tokenizer"].encode(text)
    # Normalize: HuggingFace Tokenizer.encode() returns an Encoding object;
    # extract .ids so the return type is always List[int].
    if hasattr(enc, "ids"):
        return enc.ids  # type: ignore
    return enc


def encode(uni: str) -> str:
    return codecs.encode(uni, encoding="punycode").decode()


def encode(
    string: str, exclude: str = ENCODE_DEFAULT_CHARS, *, keep_escaped: bool = True
) -> str:
    result = ""

    cache = get_encode_cache(exclude)

    l = len(string)  # noqa: E741
    i = 0
    while i < l:
        code = ord(string[i])

        #                              %
        if keep_escaped and code == 0x25 and i + 2 < l:
            if all(c in hexdigits for c in string[i + 1 : i + 3]):
                result += string[i : i + 3]
                i += 2
                i += 1  # JS for loop statement3
                continue

        if code < 128:
            result += cache[code]
            i += 1  # JS for loop statement3
            continue

        if code >= 0xD800 and code <= 0xDFFF:
            if code >= 0xD800 and code <= 0xDBFF and i + 1 < l:
                next_code = ord(string[i + 1])
                if next_code >= 0xDC00 and next_code <= 0xDFFF:
                    result += encode_uri_component(string[i] + string[i + 1])
                    i += 1
                    i += 1  # JS for loop statement3
                    continue
            result += "%EF%BF%BD"
            i += 1  # JS for loop statement3
            continue

        result += encode_uri_component(string[i])
        i += 1  # JS for loop statement3

    return result


def encode(pos, b_box):
    """returns a code that defines position with respect to a bounding box"""
    # we use the fact that python interprets booleans (the inequalities)
    # as 0/1, and then multiply them with the xxx_EDGE flags
    return (
        (pos[0] < b_box.left) * LEFT_EDGE
        + (pos[0] > b_box.right) * RIGHT_EDGE
        + (pos[1] < b_box.top) * TOP_EDGE
        + (pos[1] > b_box.bottom) * BOTTOM_EDGE
    )


def encode(input, encoding=UTF8, errors='strict'):
    """
    Encode a single string.

    :param input: An Unicode string.
    :param encoding: An :class:`Encoding` object or a label string.
    :param errors: Type of error handling. See :func:`codecs.register`.
    :raises: :exc:`~exceptions.LookupError` for an unknown encoding label.
    :return: A byte string.

    """
    return _get_encoding(encoding).codec_info.encode(input, errors)[0]


def encode(
    s: Union[str, bytes, bytearray],
    strict: bool = False,
    uts46: bool = False,
    std3_rules: bool = False,
    transitional: bool = False,
) -> bytes:
    if not isinstance(s, str):
        try:
            s = str(s, "ascii")
        except UnicodeDecodeError:
            raise IDNAError("should pass a unicode string to the function rather than a byte string.")
    if uts46:
        s = uts46_remap(s, std3_rules, transitional)
    trailing_dot = False
    result = []
    if strict:
        labels = s.split(".")
    else:
        labels = _unicode_dots_re.split(s)
    if not labels or labels == [""]:
        raise IDNAError("Empty domain")
    if labels[-1] == "":
        del labels[-1]
        trailing_dot = True
    for label in labels:
        s = alabel(label)
        if s:
            result.append(s)
        else:
            raise IDNAError("Empty label")
    if trailing_dot:
        result.append(b"")
    s = b".".join(result)
    if not valid_string_length(s, trailing_dot):
        raise IDNAError("Domain too long")
    return s


def encode(a, encoding=None, errors=None):
    """
    Calls :meth:`str.encode` element-wise.

    The set of available codecs comes from the Python standard library,
    and may be extended at runtime. For more information, see the
    :mod:`codecs` module.

    Parameters
    ----------
    a : array_like, with ``StringDType`` or ``str_`` dtype

    encoding : str, optional
       The name of an encoding

    errors : str, optional
       Specifies how to handle encoding errors

    Returns
    -------
    out : ndarray

    See Also
    --------
    str.encode

    Notes
    -----
    The type of the result will depend on the encoding specified.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array(['aAaAaA', '  aA  ', 'abBABba'])
    >>> np.strings.encode(a, encoding='cp037')
    array([b'\x81\xc1\x81\xc1\x81\xc1', b'@@\x81\xc1@@',
       b'\x81\x82\xc2\xc1\xc2\x82\x81'], dtype='|S7')

    """
    return _to_bytes_or_str_array(
        _vec_string(a, np.object_, 'encode', _clean_args(encoding, errors)),
        np.bytes_(b''))


def encode(provider: str, unified_uuid: str, raw_provider_id: str) -> str:
    """Return a urlsafe-base64 managed ID string (trailing ``=`` stripped)."""
    plaintext = SpecialEnums.LITELLM_PASSTHROUGH_MANAGED_ID_COMPLETE_STR.value.format(
        provider, unified_uuid, raw_provider_id
    )
    return base64.urlsafe_b64encode(plaintext.encode()).decode().rstrip("=")


def encode(signer, payload, header=None, key_id=None):
    """Make a signed JWT.

    Args:
        signer (google.auth.crypt.Signer): The signer used to sign the JWT.
        payload (Mapping[str, str]): The JWT payload.
        header (Mapping[str, str]): Additional JWT header payload.
        key_id (str): The key id to add to the JWT header. If the
            signer has a key id it will be used as the default. If this is
            specified it will override the signer's key id.

    Returns:
        bytes: The encoded JWT.
    """
    if header is None:
        header = {}

    if key_id is None:
        key_id = signer.key_id

    header.update({"typ": "JWT"})

    if "alg" not in header:
        if es is not None and isinstance(signer, es.EsSigner):
            header.update({"alg": signer.algorithm})
        else:
            header.update({"alg": "RS256"})

    if key_id is not None:
        header["kid"] = key_id

    segments = [
        _helpers.unpadded_urlsafe_b64encode(json.dumps(header).encode("utf-8")),
        _helpers.unpadded_urlsafe_b64encode(json.dumps(payload).encode("utf-8")),
    ]

    signing_input = b".".join(segments)
    signature = signer.sign(signing_input)
    segments.append(_helpers.unpadded_urlsafe_b64encode(signature))

    return b".".join(segments)


def encode(signer, payload, header=None, key_id=None):
    """Make a signed JWT.

    Args:
        signer (google.auth.crypt.Signer): The signer used to sign the JWT.
        payload (Mapping[str, str]): The JWT payload.
        header (Mapping[str, str]): Additional JWT header payload.
        key_id (str): The key id to add to the JWT header. If the
            signer has a key id it will be used as the default. If this is
            specified it will override the signer's key id.

    Returns:
        bytes: The encoded JWT.
    """
    return jwt.encode(signer, payload, header, key_id)


def encode(values: Iterable[int]) -> bytes:
    """Encode a set of integers as a sparse bit set.

    Tries all branching factors and returns the shortest encoding.

    Args:
        values: iterable of non-negative integers.

    Returns:
        bytes containing the sparse bit set encoding.
    """
    valuesSorted = sorted(set(values))
    if not valuesSorted:
        return _encodeHeader(2, 0)

    maxValue = valuesSorted[-1]
    valueSet = set(valuesSorted)

    best: Optional[bytes] = None
    for branchFactor in (2, 4, 8, 32):
        height = _treeHeight(branchFactor, maxValue)
        if height > _BF_MAX_HEIGHT[branchFactor]:
            continue
        encoded = _encodeWithBf(valueSet, branchFactor, height)
        if best is None or len(encoded) < len(best):
            best = encoded

    if best is None:
        raise ValueError(f"Cannot encode max value {maxValue}")
    return best

