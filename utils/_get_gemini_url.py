from typing import Optional, Tuple

def _get_gemini_url(
    mode: all_gemini_url_modes,
    model: str,
    stream: Optional[bool],
) -> Tuple[str, str]:
    """Build the Gemini API URL for the given mode.

    The API key is NOT included in the URL. Callers must pass it via the
    ``x-goog-api-key`` header instead to avoid leaking credentials in
    error tracebacks.
    """
    from litellm.llms.vertex_ai.gemini.vertex_and_google_ai_studio_gemini import (
        VertexGeminiConfig,
    )

    _gemini_model_name = "models/{}".format(model)
    api_version = (
        "v1alpha" if VertexGeminiConfig._is_gemini_3_or_newer(model) else "v1beta"
    )

    if mode == "chat":
        endpoint = "generateContent"
        if stream is True:
            endpoint = "streamGenerateContent"
            url = "https://generativelanguage.googleapis.com/{}/{}:{}?alt=sse".format(
                api_version, _gemini_model_name, endpoint
            )
        else:
            url = "https://generativelanguage.googleapis.com/{}/{}:{}".format(
                api_version, _gemini_model_name, endpoint
            )
    elif mode == "embedding":
        endpoint = "embedContent"
        url = "https://generativelanguage.googleapis.com/v1beta/{}:{}".format(
            _gemini_model_name, endpoint
        )
    elif mode == "batch_embedding":
        endpoint = "batchEmbedContents"
        url = "https://generativelanguage.googleapis.com/v1beta/{}:{}".format(
            _gemini_model_name, endpoint
        )
    elif mode == "count_tokens":
        endpoint = "countTokens"
        url = "https://generativelanguage.googleapis.com/v1beta/{}:{}".format(
            _gemini_model_name, endpoint
        )
    elif mode == "image_generation":
        raise ValueError(
            "LiteLLM's `gemini/` route does not support image generation yet. Let us know if you need this feature by opening an issue at https://github.com/BerriAI/litellm/issues"
        )
    else:
        raise ValueError(f"Unsupported mode: {mode}")

    return url, endpoint

