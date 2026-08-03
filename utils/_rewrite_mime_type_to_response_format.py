from typing import Any, Dict

def _rewrite_mime_type_to_response_format(generation_config: GenerationConfig) -> None:
    """
    Convert response_mime_type + response_json_schema/response_schema to the newer
    responseFormat structure when googleMaps is present in tools.

    The Gemini API rejects the combination of googleMaps + response_mime_type:
    'application/json' with the error:
        "Google Maps tool with a response mime type: 'application/json' is unsupported"

    The newer responseFormat field supports this combination on both the Gemini API
    (generativelanguage.googleapis.com) and Vertex AI endpoints.

    Before:
        generationConfig: {
            response_mime_type: "application/json",
            response_json_schema: {...}
        }

    After:
        generationConfig: {
            responseFormat: {
                "text": {"mimeType": "APPLICATION_JSON", "schema": {...}}
            }
        }
    """
    schema = generation_config.pop("response_json_schema", None)  # type: ignore[misc]
    if schema is None:
        schema = generation_config.pop("response_schema", None)  # type: ignore[misc]
    generation_config.pop("response_mime_type", None)  # type: ignore[misc]

    response_format: Dict[str, Any] = {"text": {"mimeType": "APPLICATION_JSON"}}
    if schema is not None:
        response_format["text"]["schema"] = schema
    generation_config["responseFormat"] = response_format  # type: ignore[typeddict-unknown-key]

