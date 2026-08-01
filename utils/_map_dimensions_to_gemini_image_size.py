
def _map_dimensions_to_gemini_image_size(width: int, height: int) -> str:
    effective_square_side = math.sqrt(width * height)
    if effective_square_side < 768:
        return "512"
    if effective_square_side < 1536:
        return "1K"
    if effective_square_side < 3072:
        return "2K"
    return "4K"

