
def _apply_gemini_metadata(
    part: PartType,
    model: Optional[str],
    media_resolution_enum: Optional[Dict[str, str]],
    video_metadata: Optional[Dict[str, Any]],
) -> PartType:
    """
    Apply media_resolution and video_metadata parameters to a Gemini part.

    - Per-part media_resolution: Gemini 3+ only (2.x uses generation_config global).
    - video_metadata (fps, startOffset, endOffset): all Gemini models (1.x, 2.x, 3+).
    """
    if model is None:
        return part

    from .vertex_and_google_ai_studio_gemini import VertexGeminiConfig

    part_dict = dict(part)

    if media_resolution_enum is not None and VertexGeminiConfig._is_gemini_3_or_newer(
        model
    ):
        part_dict["media_resolution"] = media_resolution_enum

    if video_metadata is not None:
        gemini_video_metadata = {}
        if "fps" in video_metadata:
            gemini_video_metadata["fps"] = video_metadata["fps"]
        if "start_offset" in video_metadata:
            gemini_video_metadata["startOffset"] = video_metadata["start_offset"]
        if "end_offset" in video_metadata:
            gemini_video_metadata["endOffset"] = video_metadata["end_offset"]
        if gemini_video_metadata:
            part_dict["video_metadata"] = gemini_video_metadata

    return cast(PartType, part_dict)

