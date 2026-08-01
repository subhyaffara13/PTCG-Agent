
def _map_dimensions_to_gemini_aspect_ratio(width: int, height: int) -> str:
    if (width, height) in GEMINI_IMAGE_SIZE_TO_ASPECT_RATIO:
        return GEMINI_IMAGE_SIZE_TO_ASPECT_RATIO[(width, height)]

    requested_ratio = width / height
    return min(
        GEMINI_IMAGE_ASPECT_RATIOS,
        key=lambda aspect_ratio: abs(
            math.log(GEMINI_IMAGE_ASPECT_RATIOS[aspect_ratio] / requested_ratio)
        ),
    )

