import functools
import re
from typing import List, Optional, Set, Tuple, Union

def decode(
    s: Union[str, bytes, bytearray],
    strict: bool = False,
    uts46: bool = False,
    std3_rules: bool = False,
    display: bool = False,
) -> str:
    """Decode an A-label-encoded domain name back to Unicode.

    Splits the input on label separators (see :func:`encode` for the
    rules), decodes each label with :func:`ulabel`, and rejoins them
    with ``.``. Optionally pre-processes the input through
    :func:`uts46_remap`.

    :param s: The domain name to decode.
    :param strict: If ``True``, only ``U+002E`` is recognised as a label
        separator.
    :param uts46: If ``True``, apply UTS #46 mapping before decoding.
    :param std3_rules: Forwarded to :func:`uts46_remap` when ``uts46`` is
        ``True``.
    :param display: If ``True``, any ``xn--`` label that fails IDNA
        validation is passed through unchanged (lowercased) rather than
        aborting the whole call. Intended for "decode for display"
        consumers (e.g. URL libraries, HTTP clients) that want to show
        the user the label as it appears on the wire when it cannot be
        rendered as Unicode. Matches the per-label recovery prescribed
        by UTS #46 §4 and the WHATWG URL "domain to Unicode" algorithm.
    :returns: The decoded domain as a Unicode string.
    :raises IDNAError: If the input is not valid ASCII, contains an
        invalid label, or is empty.
    """
    if not isinstance(s, str):
        try:
            s = str(s, "ascii")
        except (UnicodeDecodeError, TypeError) as err:
            raise IDNAError("Invalid ASCII in A-label") from err
    if len(s) > _max_input_length:
        raise IDNAError("Domain too long")
    if uts46:
        s = uts46_remap(s, std3_rules, False)
    # Reject inputs that exceed the maximum DNS domain length up-front
    # to avoid expensive computation on long inputs.
    if not valid_string_length(s, trailing_dot=True):
        raise IDNAError("Domain too long")
    trailing_dot = False
    result = []
    labels = s.split(".") if strict else _unicode_dots_re.split(s)
    if not labels or labels == [""]:
        raise IDNAError("Empty domain")
    if not labels[-1]:
        del labels[-1]
        trailing_dot = True
    for label in labels:
        try:
            u = ulabel(label)
        except IDNAError:
            if display and label[:4].lower() == "xn--":
                u = label.lower()
            else:
                raise
        if u:
            result.append(u)
        else:
            raise IDNAError("Empty label")
    if trailing_dot:
        result.append("")
    return ".".join(result)


def decode(
    model="",
    tokens: List[int] = [],
    custom_tokenizer: Optional[dict] = None,
    skip_special_tokens: bool = True,
):
    """
    Decodes token ids using the selected tokenizer.

    Args:
        skip_special_tokens: For HuggingFace tokenizers, keep the historical
            LiteLLM round-trip behavior by omitting special tokens by default.
            Set to False to inspect decoded BOS/EOS tokens.
    """
    tokenizer_json = custom_tokenizer or _select_tokenizer(model=model)
    if tokenizer_json["type"] == "huggingface_tokenizer":
        if skip_special_tokens:
            tokens = _strip_huggingface_special_token_ids(
                tokenizer_json["tokenizer"], tokens
            )
        dec = tokenizer_json["tokenizer"].decode(
            tokens, skip_special_tokens=skip_special_tokens
        )
        return dec
    dec = tokenizer_json["tokenizer"].decode(tokens)
    return dec


def decode(ascii: str) -> str:
    return codecs.decode(ascii, encoding="punycode")  # type: ignore


def decode(string: str, exclude: str = DECODE_DEFAULT_CHARS) -> str:
    cache = get_decode_cache(exclude)
    repl_func = functools.partial(repl_func_with_cache, cache=cache)
    return re.sub(r"(%[a-f0-9]{2})+", repl_func, string, flags=re.IGNORECASE)


def decode(s):
    return s.decode(encoding=ENCODING, errors=ENCODING_ERRS)


def decode(string: str | bytes, encodings: list[str] | None = None) -> str:
    if not isinstance(string, bytes):
        return string

    encodings = encodings or ["utf-8", "latin1", "ascii"]

    for encoding in encodings:
        with contextlib.suppress(UnicodeEncodeError, UnicodeDecodeError):
            return string.decode(encoding)

    return string.decode(encodings[0], errors="ignore")


def decode(input, fallback_encoding, errors='replace'):
    """
    Decode a single string.

    :param input: A byte string
    :param fallback_encoding:
        An :class:`Encoding` object or a label string.
        The encoding to use if :obj:`input` does note have a BOM.
    :param errors: Type of error handling. See :func:`codecs.register`.
    :raises: :exc:`~exceptions.LookupError` for an unknown encoding label.
    :return:
        A ``(output, encoding)`` tuple of an Unicode string
        and an :obj:`Encoding`.

    """
    # Fail early if `encoding` is an invalid label.
    fallback_encoding = _get_encoding(fallback_encoding)
    bom_encoding, input = _detect_bom(input)
    encoding = bom_encoding or fallback_encoding
    return encoding.codec_info.decode(input, errors)[0], encoding


def decode(
    s: Union[str, bytes, bytearray],
    strict: bool = False,
    uts46: bool = False,
    std3_rules: bool = False,
) -> str:
    try:
        if not isinstance(s, str):
            s = str(s, "ascii")
    except UnicodeDecodeError:
        raise IDNAError("Invalid ASCII in A-label")
    if uts46:
        s = uts46_remap(s, std3_rules, False)
    trailing_dot = False
    result = []
    if not strict:
        labels = _unicode_dots_re.split(s)
    else:
        labels = s.split(".")
    if not labels or labels == [""]:
        raise IDNAError("Empty domain")
    if not labels[-1]:
        del labels[-1]
        trailing_dot = True
    for label in labels:
        s = ulabel(label)
        if s:
            result.append(s)
        else:
            raise IDNAError("Empty label")
    if trailing_dot:
        result.append("")
    return ".".join(result)


def decode(a, encoding=None, errors=None):
    r"""
    Calls :meth:`bytes.decode` element-wise.

    The set of available codecs comes from the Python standard library,
    and may be extended at runtime.  For more information, see the
    :mod:`codecs` module.

    Parameters
    ----------
    a : array_like, with ``bytes_`` dtype

    encoding : str, optional
       The name of an encoding

    errors : str, optional
       Specifies how to handle encoding errors

    Returns
    -------
    out : ndarray

    See Also
    --------
    :py:meth:`bytes.decode`

    Notes
    -----
    The type of the result will depend on the encoding specified.

    Examples
    --------
    >>> import numpy as np
    >>> c = np.array([b'\x81\xc1\x81\xc1\x81\xc1', b'@@\x81\xc1@@',
    ...               b'\x81\x82\xc2\xc1\xc2\x82\x81'])
    >>> c
    array([b'\x81\xc1\x81\xc1\x81\xc1', b'@@\x81\xc1@@',
           b'\x81\x82\xc2\xc1\xc2\x82\x81'], dtype='|S7')
    >>> np.strings.decode(c, encoding='cp037')
    array(['aAaAaA', '  aA  ', 'abBABba'], dtype='<U7')

    """
    return _to_bytes_or_str_array(
        _vec_string(a, np.object_, 'decode', _clean_args(encoding, errors)),
        np.str_(''))


def decode(managed_id: str) -> Optional[ManagedIdPayload]:
    """
    Decode *managed_id*.

    Returns ``None`` for anything that is not a passthrough managed ID — raw
    OpenAI IDs, unified-endpoint IDs, garbage, wrong types.  Never raises.
    """
    if not isinstance(managed_id, str):
        return None
    # Restore stripped padding before decoding
    padded = managed_id + "=" * (-len(managed_id) % 4)
    try:
        plaintext = base64.urlsafe_b64decode(padded).decode()
    except Exception:
        return None

    # Must start with "litellm_proxy:passthrough;"
    expected_head = f"{_PREFIX}:{_DISCRIMINATOR};"
    if not plaintext.startswith(expected_head):
        return None

    rest = plaintext[len(expected_head) :]
    try:
        # Split only on first two ';' so a raw_id containing ';' cannot
        # break parsing (OpenAI IDs don't use ';', but defensive).
        provider_part, rest2 = rest.split(";", 1)
        unified_part, raw_id_part = rest2.split(";", 1)
        if not (
            provider_part.startswith("provider:")
            and unified_part.startswith("unified_id,")
            and raw_id_part.startswith("raw_id,")
        ):
            return None
        return ManagedIdPayload(
            provider=provider_part[len("provider:") :],
            unified_uuid=unified_part[len("unified_id,") :],
            raw_provider_id=raw_id_part[len("raw_id,") :],
        )
    except Exception:
        return None


def decode(token, certs=None, verify=True, audience=None, clock_skew_in_seconds=0):
    """Decode and verify a JWT.

    Args:
        token (str): The encoded JWT.
        certs (Union[str, bytes, Mapping[str, Union[str, bytes]]]): The
            certificate used to validate the JWT signature. If bytes or string,
            it must the the public key certificate in PEM format. If a mapping,
            it must be a mapping of key IDs to public key certificates in PEM
            format. The mapping must contain the same key ID that's specified
            in the token's header.
        verify (bool): Whether to perform signature and claim validation.
            Verification is done by default.
        audience (str or list): The audience claim, 'aud', that this JWT should
            contain. Or a list of audience claims. If None then the JWT's 'aud'
            parameter is not verified.
        clock_skew_in_seconds (int): The clock skew used for `iat` and `exp`
            validation.

    Returns:
        Mapping[str, str]: The deserialized JSON payload in the JWT.

    Raises:
        google.auth.exceptions.InvalidValue: if value validation failed.
        google.auth.exceptions.MalformedError: if schema validation failed.
    """
    header, payload, signed_section, signature = _unverified_decode(token)

    if not verify:
        return payload

    # Pluck the key id and algorithm from the header and make sure we have
    # a verifier that can support it.
    key_alg = header.get("alg")
    key_id = header.get("kid")

    try:
        verifier_cls = _ALGORITHM_TO_VERIFIER_CLASS[key_alg]
    except KeyError as exc:
        if key_alg in _CRYPTOGRAPHY_BASED_ALGORITHMS:
            raise exceptions.InvalidValue(
                "The key algorithm {} requires the cryptography package to be installed.".format(
                    key_alg
                )
            ) from exc
        else:
            raise exceptions.InvalidValue(
                "Unsupported signature algorithm {}".format(key_alg)
            ) from exc
    # If certs is specified as a dictionary of key IDs to certificates, then
    # use the certificate identified by the key ID in the token header.
    if isinstance(certs, Mapping):
        if key_id:
            if key_id not in certs:
                raise exceptions.MalformedError(
                    "Certificate for key id {} not found.".format(key_id)
                )
            certs_to_check = [certs[key_id]]
        # If there's no key id in the header, check against all of the certs.
        else:
            certs_to_check = certs.values()
    else:
        certs_to_check = certs

    # Verify that the signature matches the message.
    if not crypt.verify_signature(
        signed_section, signature, certs_to_check, verifier_cls
    ):
        raise exceptions.MalformedError("Could not verify token signature.")

    # Verify the issued at and created times in the payload.
    _verify_iat_and_exp(payload, clock_skew_in_seconds)

    # Check audience.
    if audience is not None:
        claim_audience = payload.get("aud")
        if isinstance(audience, str):
            audience = [audience]
        if claim_audience not in audience:
            raise exceptions.InvalidValue(
                "Token has wrong audience {}, expected one of {}".format(
                    claim_audience, audience
                )
            )

    return payload


def decode(token, certs=None, verify=True, audience=None):
    """Decode and verify a JWT.

    Args:
        token (str): The encoded JWT.
        certs (Union[str, bytes, Mapping[str, Union[str, bytes]]]): The
            certificate used to validate the JWT signature. If bytes or string,
            it must the the public key certificate in PEM format. If a mapping,
            it must be a mapping of key IDs to public key certificates in PEM
            format. The mapping must contain the same key ID that's specified
            in the token's header.
        verify (bool): Whether to perform signature and claim validation.
            Verification is done by default.
        audience (str): The audience claim, 'aud', that this JWT should
            contain. If None then the JWT's 'aud' parameter is not verified.

    Returns:
        Mapping[str, str]: The deserialized JSON payload in the JWT.

    Raises:
        ValueError: if any verification checks failed.
    """

    return jwt.decode(token, certs, verify, audience)


def decode(
    data: bytes, bias: int = 0, maxValue: int = 0xFFFFFFFF
) -> Tuple[Set[int], int]:
    """Decode a sparse bit set from binary data.

    Args:
        data: bytes-like object containing the sparse bit set encoding.
        bias: integer added to each decoded value.

    Returns:
        A tuple (values, bytesConsumed) where values is a set of integers
        and bytesConsumed is the number of bytes read from data.
    """
    if not data:
        raise SparseBitSetDecodeError("Empty data")

    branchFactor, height = _decodeHeader(data[0])

    maxHeight = _BF_MAX_HEIGHT[branchFactor]
    if height > maxHeight:
        raise SparseBitSetDecodeError(
            f"Height {height} exceeds max {maxHeight} for branch factor {branchFactor}"
        )

    return _decodeImpl(data, branchFactor, height, bias, maxValue)

