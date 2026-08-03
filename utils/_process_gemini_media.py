import os
from typing import Any, Dict, Optional

def _process_gemini_media(
    image_url: str,
    format: Optional[str] = None,
    media_resolution_enum: Optional[Dict[str, str]] = None,
    model: Optional[str] = None,
    video_metadata: Optional[Dict[str, Any]] = None,
    vertex_project: Optional[str] = None,
    vertex_credentials: Optional[Any] = None,
) -> PartType:
    """
    Given a media URL (image, audio, or video), return the appropriate PartType for Gemini
    By the way, actually video_metadata can only be used with videos; it cannot be used with images, audio, or files. However, I haven't made any special handling because vertex returns a parameter error.

    Args:
        image_url: The URL or base64 string of the media (image, audio, or video)
        format: The MIME type of the media
        media_resolution_enum: Media resolution level (for Gemini 3+)
        model: The model name (to check version compatibility)
        video_metadata: Video-specific metadata (fps, start_offset, end_offset)
    """

    try:
        # GCS URIs
        if "gs://" in image_url:
            extension_with_dot = os.path.splitext(image_url)[-1]  # Ex: ".png"
            extension = extension_with_dot[1:]  # Ex: "png"

            explicit_gcs_format = False
            if not format:
                mime_type: Optional[str] = None
                # For extension-less gs:// URIs, we cannot infer from path.
                # If callers pass `format`/`mime_type`, this branch is skipped.
                if extension:
                    file_type = get_file_type_from_extension(extension)

                    # Validate the file type is supported by Gemini
                    if not is_gemini_1_5_accepted_file_type(file_type):
                        raise litellm.BadRequestError(
                            message=f"File type not supported by gemini - {file_type}",
                            model=model,
                            llm_provider="vertex_ai",
                        )

                    mime_type = get_file_mime_type_for_file_type(file_type)
                else:
                    mime_type = _get_gcs_object_content_type(
                        image_url=image_url,
                        vertex_project=vertex_project,
                        vertex_credentials=vertex_credentials,
                    )
                    if mime_type is None:
                        raise litellm.BadRequestError(
                            message=(
                                f"Unable to determine mime type for gs URI: {image_url}. "
                                "This gs:// URI has no file extension and GCS metadata "
                                "lookup failed. Set it explicitly using image_url.format "
                                "(or image_url.mime_type/content_type) or "
                                "message.content[].file.format."
                            ),
                            model=model,
                            llm_provider="vertex_ai",
                        )
            else:
                mime_type = format
                explicit_gcs_format = True
            if mime_type is None:
                raise litellm.BadRequestError(
                    message=f"File type not supported by gemini - {image_url}",
                    model=model,
                    llm_provider="vertex_ai",
                )
            if explicit_gcs_format:
                # Callers who pass format/mime_type explicitly for gs:// URIs
                # rely on pass-through to Gemini (pre-PR behavior). Only apply
                # known MIME aliases; skip litellm's file-type registry.
                mime_type = _apply_gemini_mime_type_aliases(mime_type)
            else:
                mime_type = _normalize_and_validate_gemini_mime_type(
                    mime_type=mime_type,
                    model=model,
                )
            file_data = FileDataType(mime_type=mime_type, file_uri=image_url)
            part: PartType = {"file_data": file_data}
            return _apply_gemini_metadata(
                part, model, media_resolution_enum, video_metadata
            )
        elif image_url.startswith(
            "https://generativelanguage.googleapis.com/v1beta/files/"
        ):
            # Gemini Files API URIs — the file is already uploaded to Google's
            # servers; pass the URI through as file_data without fetching it.
            # These URLs return 403 when accessed directly, so we must not try
            # to resolve their MIME type via HTTP.
            if format:
                file_data = FileDataType(mime_type=format, file_uri=image_url)
            else:
                # Gemini Files API references can be passed through as URI-only.
                file_data = cast(FileDataType, {"file_uri": image_url})
            part = {"file_data": file_data}
            return _apply_gemini_metadata(
                part, model, media_resolution_enum, video_metadata
            )
        elif (
            "https://" in image_url
            and (image_type := format or _get_image_mime_type_from_url(image_url))
            is not None
        ):
            file_data = FileDataType(mime_type=image_type, file_uri=image_url)
            part = {"file_data": file_data}
            return _apply_gemini_metadata(
                part, model, media_resolution_enum, video_metadata
            )
        elif "http://" in image_url or "https://" in image_url or "base64" in image_url:
            image = convert_to_anthropic_image_obj(image_url, format=format)
            _blob: BlobType = {"data": image["data"], "mime_type": image["media_type"]}
            part = {"inline_data": cast(BlobType, _blob)}
            return _apply_gemini_metadata(
                part, model, media_resolution_enum, video_metadata
            )
        raise Exception("Invalid image received - {}".format(image_url))
    except Exception as e:
        raise e

