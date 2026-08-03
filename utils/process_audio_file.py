import os

def process_audio_file(audio_file: FileTypes) -> ProcessedAudioFile:
    """
    Common utility function to process audio files for audio transcription APIs.

    Handles various input types:
    - File paths (str, os.PathLike)
    - Raw bytes/bytearray
    - Tuples (filename, content, optional content_type)
    - File-like objects with read() method

    Args:
        audio_file: The audio file input in various formats

    Returns:
        ProcessedAudioFile: Structured data with file content, filename, and content type

    Raises:
        ValueError: If audio_file type is unsupported or content cannot be extracted
    """
    file_content = None
    filename = None

    if isinstance(audio_file, (bytes, bytearray)):
        # Raw bytes
        filename = "audio.wav"
        file_content = bytes(audio_file)
    elif isinstance(audio_file, str):
        # Bare strings are rejected — see extract_file_data for the same
        # rationale: in a proxy request handler the string is
        # attacker-controlled, and opening it as a path is an arbitrary
        # file read.
        raise ValueError(
            "process_audio_file does not accept bare str inputs. Pass bytes, "
            "an open file handle, a (filename, content) tuple, or a "
            "pathlib.Path."
        )
    elif isinstance(audio_file, os.PathLike):
        # File path or PathLike — PathLike is a Python-level type that
        # HTTP form values can't fabricate.
        file_path = str(audio_file)
        with open(file_path, "rb") as f:
            file_content = f.read()
        filename = file_path.split("/")[-1]
    elif isinstance(audio_file, tuple):
        # Tuple format: (filename, content, content_type) or (filename, content)
        if len(audio_file) >= 2:
            filename = audio_file[0] or "audio.wav"
            content = audio_file[1]
            if isinstance(content, (bytes, bytearray)):
                file_content = bytes(content)
            elif isinstance(content, str):
                raise ValueError(
                    "process_audio_file does not accept bare str tuple "
                    "contents. Pass bytes, an open file handle, or a "
                    "pathlib.Path."
                )
            elif isinstance(content, os.PathLike):
                # PathLike: SDK convenience for local-file uploads.
                with open(str(content), "rb") as f:
                    file_content = f.read()
            elif hasattr(content, "read"):
                # File-like object
                file_content = content.read()
                if hasattr(content, "seek"):
                    content.seek(0)
            else:
                raise ValueError(f"Unsupported content type in tuple: {type(content)}")
        else:
            raise ValueError("Tuple must have at least 2 elements: (filename, content)")
    elif hasattr(audio_file, "read") and not isinstance(
        audio_file, (str, bytes, bytearray, tuple, os.PathLike)
    ):
        # File-like object (IO) - check this after all other types
        filename = getattr(audio_file, "name", "audio.wav")
        file_content = audio_file.read()  # type: ignore
        # Reset file pointer if possible
        if hasattr(audio_file, "seek"):
            audio_file.seek(0)  # type: ignore
    else:
        raise ValueError(f"Unsupported audio_file type: {type(audio_file)}")

    if file_content is None:
        raise ValueError("Could not extract file content from audio_file")

    # Determine content type using LiteLLM's file type utilities
    content_type = "audio/wav"  # Default fallback
    if filename:
        try:
            # Extract extension from filename
            extension = filename.split(".")[-1].lower() if "." in filename else "wav"
            content_type = get_file_mime_type_from_extension(extension)
        except ValueError:
            # If extension is not recognized, fallback to audio/wav
            content_type = "audio/wav"

    return ProcessedAudioFile(
        file_content=file_content, filename=filename, content_type=content_type
    )

