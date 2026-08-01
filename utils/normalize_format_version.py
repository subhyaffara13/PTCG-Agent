
def normalizeFormatVersion(
    value: FormatVersionInput, cls: Type[FormatVersion]
) -> FormatVersion:
    # Needed for type safety of UFOFormatVersion and GLIFFormatVersion input
    if value is None:
        return cls.default()
    if isinstance(value, cls):
        return value
    if isinstance(value, int):
        return cls((value, 0))
    if isinstance(value, tuple) and len(value) == 2:
        return cls(value)
    raise ValueError(f"Unsupported format version: {value!r}")

