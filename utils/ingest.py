from typing import Any, Dict, Optional, Tuple, Union

def ingest(
    ingest_options: Dict[str, Any],
    file_data: Optional[Tuple[str, bytes, str]] = None,
    file: Optional[Dict[str, str]] = None,
    file_url: Optional[str] = None,
    file_id: Optional[str] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    **kwargs,
) -> Union[RAGIngestResponse, Coroutine[Any, Any, RAGIngestResponse]]:
    """
    Ingest a document into a vector store.

    Args:
        ingest_options: Configuration for the ingest pipeline
        file_data: Tuple of (filename, content_bytes, content_type)
        file: Dict with {filename, content (base64), content_type} - for JSON API
        file_url: URL to fetch file from
        file_id: Existing file ID to use

    Example:
        ```python
        response = litellm.ingest(
            ingest_options={
                "vector_store": {
                    "custom_llm_provider": "openai",
                    "litellm_credential_name": "my-openai-creds",  # optional
                }
            },
            file_data=("doc.txt", b"Hello world", "text/plain"),
        )
        ```
    """
    import base64

    local_vars = locals()
    try:
        _is_async = kwargs.pop("aingest", False) is True
        router: Optional["Router"] = kwargs.get("router")

        # Convert file dict to file_data tuple if provided
        if file is not None and file_data is None:
            filename = file.get("filename", "document")
            content_b64 = file.get("content", "")
            content_type = file.get("content_type", "application/octet-stream")
            content_bytes = base64.b64decode(content_b64)
            file_data = (filename, content_bytes, content_type)

        if _is_async:
            return _execute_ingest_pipeline(
                ingest_options=ingest_options,  # type: ignore
                file_data=file_data,
                file_url=file_url,
                file_id=file_id,
                router=router,
            )
        else:
            return asyncio.get_event_loop().run_until_complete(
                _execute_ingest_pipeline(
                    ingest_options=ingest_options,  # type: ignore
                    file_data=file_data,
                    file_url=file_url,
                    file_id=file_id,
                    router=router,
                )
            )
    except Exception as e:
        raise litellm.exception_type(
            model=None,
            custom_llm_provider=ingest_options.get("vector_store", {}).get(
                "custom_llm_provider"
            ),
            original_exception=e,
            completion_kwargs=local_vars,
            extra_kwargs=kwargs,
        )

