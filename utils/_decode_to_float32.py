import os
from typing import Tuple

def _decode_to_float32(file_bytes: bytes) -> Tuple["FloatArray", int]:
    """
    Decode arbitrary audio bytes into a float32 array shaped either
    ``(n_samples,)`` (mono) or ``(n_samples, n_channels)`` plus the source
    sample rate.

    Tries ``soundfile`` first (wav/flac/ogg), then falls back to
    ``audioread`` for compressed formats. Raises a clear error if neither
    works.
    """
    import numpy as np  # type: ignore

    sf_error: Exception | None = None
    try:
        import soundfile as sf  # type: ignore

        with io.BytesIO(file_bytes) as buf:
            data, source_rate = sf.read(buf, dtype="float32", always_2d=False)
        return cast("FloatArray", data), int(source_rate)
    except ImportError as e:
        sf_error = e
    except Exception as e:
        # soundfile raises RuntimeError / LibsndfileError for formats it
        # cannot decode (mp3 on older libsndfile, m4a, webm, ...).
        sf_error = e

    try:
        import audioread  # type: ignore
    except ImportError as e:
        raise NvidiaRivaException(
            status_code=400,
            message=(
                "Could not decode audio for Riva STT. Install audio extras "
                f"(`pip install 'litellm[stt-nvidia-riva]'`) or convert your "
                f"audio to wav/flac/ogg before calling the API. "
                f"Underlying error: {sf_error}"
            ),
        ) from e

    # audioread backends (FFmpeg subprocess, GStreamer, Core Audio) require a
    # filesystem path, so spill the bytes to a temp file. mkstemp is portable
    # to Windows where re-opening a NamedTemporaryFile is not allowed.
    fd, tmp_path = tempfile.mkstemp(suffix=".audio")
    try:
        with os.fdopen(fd, "wb") as tmp_file:
            tmp_file.write(file_bytes)
        try:
            with audioread.audio_open(tmp_path) as src:
                source_rate = int(src.samplerate)
                channels = int(src.channels)
                chunks = []
                for buf in src:
                    chunks.append(np.frombuffer(buf, dtype=np.int16))
                if not chunks:
                    raise NvidiaRivaException(
                        status_code=400,
                        message="Audio decode produced no samples.",
                    )
                interleaved = np.concatenate(chunks).astype(np.float32) / 32768.0
                if channels > 1:
                    interleaved = interleaved.reshape(-1, channels)
                return cast("FloatArray", interleaved), source_rate
        except NvidiaRivaException:
            raise
        except Exception as e:
            raise NvidiaRivaException(
                status_code=400,
                message=(
                    "Could not decode audio for Riva STT. Convert your audio to "
                    f"wav/flac/ogg before calling the API. Underlying error: {e}"
                ),
            ) from e
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass

