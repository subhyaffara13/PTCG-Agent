
def is_binary(
    fp_or_path_or_payload: PathLike | str | BinaryIO | bytes,  # type: ignore[type-arg]
    steps: int = 5,
    chunk_size: int = 512,
    threshold: float = 0.20,
    cp_isolation: list[str] | None = None,
    cp_exclusion: list[str] | None = None,
    preemptive_behaviour: bool = True,
    explain: bool = False,
    language_threshold: float = 0.1,
    enable_fallback: bool = False,
) -> bool:
    """
    Detect if the given input (file, bytes, or path) points to a binary file. aka. not a string.
    Based on the same main heuristic algorithms and default kwargs at the sole exception that fallbacks match
    are disabled to be stricter around ASCII-compatible but unlikely to be a string.
    """
    if isinstance(fp_or_path_or_payload, (str, PathLike)):
        guesses = from_path(
            fp_or_path_or_payload,
            steps=steps,
            chunk_size=chunk_size,
            threshold=threshold,
            cp_isolation=cp_isolation,
            cp_exclusion=cp_exclusion,
            preemptive_behaviour=preemptive_behaviour,
            explain=explain,
            language_threshold=language_threshold,
            enable_fallback=enable_fallback,
        )
    elif isinstance(
        fp_or_path_or_payload,
        (
            bytes,
            bytearray,
        ),
    ):
        guesses = from_bytes(
            fp_or_path_or_payload,
            steps=steps,
            chunk_size=chunk_size,
            threshold=threshold,
            cp_isolation=cp_isolation,
            cp_exclusion=cp_exclusion,
            preemptive_behaviour=preemptive_behaviour,
            explain=explain,
            language_threshold=language_threshold,
            enable_fallback=enable_fallback,
        )
    else:
        guesses = from_fp(
            fp_or_path_or_payload,
            steps=steps,
            chunk_size=chunk_size,
            threshold=threshold,
            cp_isolation=cp_isolation,
            cp_exclusion=cp_exclusion,
            preemptive_behaviour=preemptive_behaviour,
            explain=explain,
            language_threshold=language_threshold,
            enable_fallback=enable_fallback,
        )

    return not guesses


def is_binary(value):
    r"""
    Return True if the value appears to be binary (that is, it's a byte
    string and isn't decodable).

    >>> is_binary(b'\xff')
    True
    >>> is_binary('\xff')
    False
    """
    return isinstance(value, bytes) and not is_decodable(value)

