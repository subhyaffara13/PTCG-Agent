
def calculate_request_duration(file: FileTypes) -> Optional[float]:
    """
    Calculate audio duration from file content.

    Args:
        file: The audio file (can be file path, bytes, or file-like object)

    Returns:
        Duration in seconds, or None if extraction fails or soundfile is not available
    """
    try:
        import soundfile as sf
    except ImportError:
        # soundfile not available, cannot extract duration
        return None

    try:
        import io

        # Handle different file input types
        file_content: Optional[bytes] = None

        if isinstance(file, (bytes, bytearray)):
            # Raw bytes
            file_content = bytes(file)
        elif isinstance(file, str):
            # Bare strings are rejected — see extract_file_data.
            raise ValueError(
                "calculate_request_duration does not accept bare str inputs. "
                "Pass bytes, an open file handle, a (filename, content) "
                "tuple, or a pathlib.Path."
            )
        elif isinstance(file, os.PathLike):
            # File path (PathLike): SDK convenience.
            with open(str(file), "rb") as f:
                file_content = f.read()
        elif isinstance(file, tuple):
            # Tuple format: (filename, content, optional content_type)
            if len(file) >= 2:
                content = file[1]
                if isinstance(content, bytes):
                    file_content = content
                elif hasattr(content, "read") and not isinstance(
                    content, (str, os.PathLike)
                ):
                    # File-like object in tuple
                    current_pos = getattr(content, "tell", lambda: None)()
                    # Seek to start to ensure we read the entire content
                    if hasattr(content, "seek"):
                        content.seek(0)
                    file_content = content.read()
                    if current_pos is not None and hasattr(content, "seek"):
                        content.seek(current_pos)
        elif hasattr(file, "read") and not isinstance(file, tuple):
            # File-like object (including BytesIO)
            current_position = file.tell() if hasattr(file, "tell") else None
            # Seek to start to ensure we read the entire content
            if hasattr(file, "seek"):
                file.seek(0)
            file_content = file.read()
            # Reset file position if possible
            if current_position is not None and hasattr(file, "seek"):
                file.seek(current_position)

        if file_content is None or not isinstance(file_content, bytes):
            return None

        # Extract duration using soundfile
        file_object = io.BytesIO(file_content)
        with sf.SoundFile(file_object) as audio:
            duration = len(audio) / audio.samplerate
            return duration

    except Exception:
        # Silently fail if duration extraction fails
        return None

