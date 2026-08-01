
def _decompression_bomb_check(size: tuple[int, int]) -> None:
    if MAX_IMAGE_PIXELS is None:
        return

    pixels = max(1, size[0]) * max(1, size[1])

    if pixels > 2 * MAX_IMAGE_PIXELS:
        msg = (
            f"Image size ({pixels} pixels) exceeds limit of {2 * MAX_IMAGE_PIXELS} "
            "pixels, could be decompression bomb DOS attack."
        )
        raise DecompressionBombError(msg)

    if pixels > MAX_IMAGE_PIXELS:
        warnings.warn(
            f"Image size ({pixels} pixels) exceeds limit of {MAX_IMAGE_PIXELS} pixels, "
            "could be decompression bomb DOS attack.",
            DecompressionBombWarning,
        )

