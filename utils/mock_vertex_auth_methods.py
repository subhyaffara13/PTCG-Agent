
def mock_vertex_auth_methods():
    """
    Monkey-patch Vertex AI auth methods to return fake tokens.
    This prevents auth failures when GCS_MOCK is enabled.

    This function is idempotent - it only patches once, even if called multiple times.
    """
    from litellm.llms.vertex_ai.vertex_llm_base import VertexBase

    # Store original methods if not already stored
    if not hasattr(VertexBase, "_original_ensure_access_token_async"):
        setattr(
            VertexBase,
            "_original_ensure_access_token_async",
            VertexBase._ensure_access_token_async,
        )
        setattr(
            VertexBase, "_original_ensure_access_token", VertexBase._ensure_access_token
        )
        setattr(
            VertexBase, "_original_get_token_and_url", VertexBase._get_token_and_url
        )

        async def _mock_ensure_access_token_async(
            self, credentials, project_id, custom_llm_provider
        ):
            """Mock async auth method - returns fake token."""
            verbose_logger.debug(
                "[GCS MOCK] Vertex AI auth: _ensure_access_token_async called"
            )
            return ("mock-gcs-token", "mock-project-id")

        def _mock_ensure_access_token(
            self, credentials, project_id, custom_llm_provider
        ):
            """Mock sync auth method - returns fake token."""
            verbose_logger.debug(
                "[GCS MOCK] Vertex AI auth: _ensure_access_token called"
            )
            return ("mock-gcs-token", "mock-project-id")

        def _mock_get_token_and_url(
            self,
            model,
            auth_header,
            vertex_credentials,
            vertex_project,
            vertex_location,
            gemini_api_key,
            stream,
            custom_llm_provider,
            api_base,
        ):
            """Mock get_token_and_url - returns fake token."""
            verbose_logger.debug("[GCS MOCK] Vertex AI auth: _get_token_and_url called")
            return ("mock-gcs-token", "https://storage.googleapis.com")

        # Patch the methods
        VertexBase._ensure_access_token_async = _mock_ensure_access_token_async  # type: ignore
        VertexBase._ensure_access_token = _mock_ensure_access_token  # type: ignore
        VertexBase._get_token_and_url = _mock_get_token_and_url  # type: ignore

        verbose_logger.debug("[GCS MOCK] Patched Vertex AI auth methods")

