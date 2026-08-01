
def get_audio_file_content_hash(file_obj: FileTypes) -> str:
    """
    Compute SHA-256 hash of audio file content for cache keys.
    Falls back to filename hash if content extraction fails.
    """
    file_content: Optional[bytes] = None
    fallback_filename: Optional[str] = None

    if isinstance(file_obj, tuple):
        if len(file_obj) < 2:
            fallback_filename = str(file_obj[0]) if len(file_obj) > 0 else None
        else:
            fallback_filename = str(file_obj[0]) if file_obj[0] is not None else None
            file_content_obj = file_obj[1]
    else:
        file_content_obj = file_obj
        fallback_filename = get_audio_file_name(file_obj)

    try:
        if isinstance(file_content_obj, (bytes, bytearray)):
            file_content = bytes(file_content_obj)
        elif isinstance(file_content_obj, str):
            # Bare strings are not treated as file paths in this helper —
            # the cache-key path is reached from request handlers where the
            # value is attacker-controlled. Fall back to hashing the string
            # itself rather than opening it.
            fallback_filename = file_content_obj
            file_content = None
        elif isinstance(file_content_obj, os.PathLike):
            try:
                with open(str(file_content_obj), "rb") as f:
                    file_content = f.read()
                if fallback_filename is None:
                    fallback_filename = str(file_content_obj)
            except (OSError, IOError):
                fallback_filename = str(file_content_obj)
                file_content = None
        elif hasattr(file_content_obj, "read"):
            try:
                current_position = (
                    file_content_obj.tell()
                    if hasattr(file_content_obj, "tell")
                    else None
                )
                if hasattr(file_content_obj, "seek"):
                    file_content_obj.seek(0)
                file_content = file_content_obj.read()  # type: ignore
                if current_position is not None and hasattr(file_content_obj, "seek"):
                    file_content_obj.seek(current_position)  # type: ignore
            except (OSError, IOError, AttributeError):
                file_content = None
        else:
            file_content = None
    except Exception:
        file_content = None

    if file_content is not None and isinstance(file_content, bytes):
        try:
            hash_object = hashlib.sha256(file_content)
            return hash_object.hexdigest()
        except Exception:
            pass

    if fallback_filename:
        hash_object = hashlib.sha256(fallback_filename.encode("utf-8"))
        return hash_object.hexdigest()

    file_obj_str = str(file_obj)
    hash_object = hashlib.sha256(file_obj_str.encode("utf-8"))
    return hash_object.hexdigest()

