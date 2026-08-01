
def cache_info() -> CacheInfo:
    """Report cache statistics."""
    return {
        "idna_encode": _idna_encode.cache_info(),
        "idna_decode": _idna_decode.cache_info(),
        "ip_address": _encode_host.cache_info(),
        "host_validate": _encode_host.cache_info(),
        "encode_host": _encode_host.cache_info(),
    }

