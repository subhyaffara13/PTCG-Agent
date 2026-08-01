
def extract_original_video_id(encoded_video_id: str) -> str:
    """Extract original video ID without encoding."""
    decoded = decode_video_id_with_provider(encoded_video_id)
    return decoded.get("video_id", encoded_video_id)

