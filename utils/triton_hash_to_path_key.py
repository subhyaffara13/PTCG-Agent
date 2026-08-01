
def triton_hash_to_path_key(key: str) -> str:
    # In early versions of Triton, the hash is directly used in the path name.
    # Later, the hash is converted to base64 before being used in the path name.
    # Later, the base64 conversion was replaced to the base32
    #
    # This code tries to import _base64 and falls back to _base32 if _base64 is unavailable.
    #
    # To handle this, try to import the to-base64-conversion function.
    # If it exists, use it; otherwise, try using _base32; if both are unavailable, use the hash directly.
    try:
        from triton.runtime.cache import _base64

        return _base64(key)
    except Exception:
        try:
            from triton.runtime.cache import _base32

            return _base32(key)
        except Exception:
            return key

