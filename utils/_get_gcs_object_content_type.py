
def _get_gcs_object_content_type(
    image_url: str,
    vertex_project: Optional[str] = None,
    vertex_credentials: Optional[Any] = None,
) -> Optional[str]:
    """
    Resolve content type from GCS object metadata.

    Only attaches a Bearer token when the caller explicitly supplies Vertex
    credentials, to avoid using the server's default Google credentials on
    the Gemini API-key (Google AI Studio) path and being used as an oracle
    for private GCS object metadata. Without explicit credentials we only
    issue an anonymous request, which only succeeds for publicly-readable
    objects.
    """
    try:
        bucket, object_name = _parse_gs_uri(image_url)
    except ValueError:
        return None
    if not _is_valid_gcs_bucket_name(bucket):
        return None

    headers: Dict[str, str] = {}
    explicit_vertex_auth_provided = (
        vertex_project is not None or vertex_credentials is not None
    )
    if explicit_vertex_auth_provided:
        try:
            access_token, _ = _get_vertex_base().get_access_token(
                credentials=vertex_credentials,
                project_id=vertex_project,
            )
            headers["Authorization"] = f"Bearer {access_token}"
        except Exception as e:
            raise litellm.BadRequestError(
                message=(
                    "Unable to fetch GCS metadata with provided Vertex credentials/project. "
                    f"Original error: {str(e)}"
                ),
                model=None,
                llm_provider="vertex_ai",
            )

    # Build the URL via httpx.URL with a fixed scheme/host and URL-encode both
    # bucket and object so CodeQL does not flag the interpolation as a
    # potential SSRF that could resolve to an arbitrary host.
    encoded_bucket = quote(bucket, safe="")
    encoded_object = quote(object_name, safe="")
    metadata_url = httpx.URL(
        scheme="https",
        host="storage.googleapis.com",
        path=f"/storage/v1/b/{encoded_bucket}/o/{encoded_object}",
        params={"fields": "contentType"},
    )
    try:
        response = _get_gcs_metadata_http_handler().get(
            url=str(metadata_url),
            headers=headers or None,
        )
    except httpx.RequestError as e:
        if explicit_vertex_auth_provided:
            raise litellm.BadRequestError(
                message=(
                    "Unable to reach GCS JSON API for object metadata with provided "
                    f"Vertex credentials. {type(e).__name__}: {e}"
                ),
                model=None,
                llm_provider="vertex_ai",
            ) from e
        return None

    if response.is_error:
        if explicit_vertex_auth_provided:
            preview = (response.text or "")[:1024]
            raise litellm.BadRequestError(
                message=(
                    "Unable to read GCS object metadata with provided Vertex credentials. "
                    f"HTTP {response.status_code}. Response body (truncated): {preview!r}"
                ),
                model=None,
                llm_provider="vertex_ai",
            )
        return None

    try:
        payload = response.json()
    except ValueError as e:
        if explicit_vertex_auth_provided:
            raise litellm.BadRequestError(
                message=(
                    "GCS metadata response was not valid JSON when using provided "
                    f"Vertex credentials (HTTP {response.status_code}). Error: {e}"
                ),
                model=None,
                llm_provider="vertex_ai",
            ) from e
        return None

    if not isinstance(payload, dict):
        if explicit_vertex_auth_provided:
            raise litellm.BadRequestError(
                message=(
                    "GCS metadata response was not a JSON object when using provided "
                    f"Vertex credentials (HTTP {response.status_code})."
                ),
                model=None,
                llm_provider="vertex_ai",
            )
        return None

    content_type = payload.get("contentType")
    if isinstance(content_type, str) and len(content_type) > 0:
        return content_type

    if explicit_vertex_auth_provided:
        preview = (response.text or "")[:1024]
        raise litellm.BadRequestError(
            message=(
                "GCS metadata JSON did not include a non-empty contentType field when "
                f"using provided Vertex credentials (HTTP {response.status_code}). "
                f"Body (truncated): {preview!r}"
            ),
            model=None,
            llm_provider="vertex_ai",
        )
    return None

