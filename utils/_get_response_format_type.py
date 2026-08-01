
def _get_response_format_type(
    response_format: AudioResponseFormat | Omit,
) -> type[Transcription | TranscriptionVerbose | TranscriptionDiarized | str]:
    if isinstance(response_format, Omit) or response_format is None:  # pyright: ignore[reportUnnecessaryComparison]
        return Transcription

    if response_format == "json":
        return Transcription
    elif response_format == "verbose_json":
        return TranscriptionVerbose
    elif response_format == "diarized_json":
        return TranscriptionDiarized
    elif response_format == "srt" or response_format == "text" or response_format == "vtt":
        return str
    elif TYPE_CHECKING:  # type: ignore[unreachable]
        assert_never(response_format)
    else:
        log.warn("Unexpected audio response format: %s", response_format)
        return Transcription


def _get_response_format_type(
    response_format: AudioResponseFormat | Omit,
) -> type[Translation | TranslationVerbose | str]:
    if isinstance(response_format, Omit) or response_format is None:  # pyright: ignore[reportUnnecessaryComparison]
        return Translation

    if response_format == "json":
        return Translation
    elif response_format == "verbose_json":
        return TranslationVerbose
    elif response_format == "srt" or response_format == "text" or response_format == "vtt":
        return str
    elif TYPE_CHECKING and response_format != "diarized_json":  # type: ignore[unreachable]
        assert_never(response_format)
    else:
        log.warning("Unexpected audio response format: %s", response_format)
        return Translation

