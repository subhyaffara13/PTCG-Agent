from typing import Optional

def _normalize_and_validate_gemini_mime_type(
    mime_type: str, model: Optional[str]
) -> str:
    # Import lazily to avoid a module-level cyclic-import alert with
    # litellm.types.files.
    from litellm.types.files import get_file_extension_from_mime_type

    normalized_mime_type = _apply_gemini_mime_type_aliases(mime_type)
    try:
        file_extension = get_file_extension_from_mime_type(normalized_mime_type)
        file_type = get_file_type_from_extension(file_extension)
    except ValueError:
        raise litellm.BadRequestError(
            message=f"File type not supported by gemini - {normalized_mime_type}",
            model=model,
            llm_provider="vertex_ai",
        )

    if not is_gemini_1_5_accepted_file_type(file_type):
        raise litellm.BadRequestError(
            message=f"File type not supported by gemini - {file_type}",
            model=model,
            llm_provider="vertex_ai",
        )

    return get_file_mime_type_for_file_type(file_type)

