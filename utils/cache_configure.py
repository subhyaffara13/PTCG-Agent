
def cache_configure(
    *,
    idna_encode_size: int | None = _DEFAULT_IDNA_SIZE,
    idna_decode_size: int | None = _DEFAULT_IDNA_SIZE,
    ip_address_size: int | None | UndefinedType = UNDEFINED,
    host_validate_size: int | None | UndefinedType = UNDEFINED,
    encode_host_size: int | None | UndefinedType = UNDEFINED,
) -> None:
    """Configure LRU cache sizes."""
    global _idna_decode, _idna_encode, _encode_host
    # ip_address_size, host_validate_size are no longer
    # used, but are kept for backwards compatibility.
    if ip_address_size is not UNDEFINED or host_validate_size is not UNDEFINED:
        warnings.warn(
            "cache_configure() no longer accepts the "
            "ip_address_size or host_validate_size arguments, "
            "they are used to set the encode_host_size instead "
            "and will be removed in the future",
            DeprecationWarning,
            stacklevel=2,
        )

    if encode_host_size is not None:
        for size in (ip_address_size, host_validate_size):
            if size is None:
                encode_host_size = None
            elif encode_host_size is UNDEFINED:
                if size is not UNDEFINED:
                    encode_host_size = size
            elif size is not UNDEFINED:
                if TYPE_CHECKING:
                    assert isinstance(size, int)
                    assert isinstance(encode_host_size, int)
                encode_host_size = max(size, encode_host_size)
        if encode_host_size is UNDEFINED:
            encode_host_size = _DEFAULT_ENCODE_SIZE

    _encode_host = lru_cache(encode_host_size)(_encode_host.__wrapped__)
    _idna_decode = lru_cache(idna_decode_size)(_idna_decode.__wrapped__)
    _idna_encode = lru_cache(idna_encode_size)(_idna_encode.__wrapped__)

