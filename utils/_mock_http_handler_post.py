
def _mock_http_handler_post(
    self,
    url,
    data=None,
    json=None,
    params=None,
    headers=None,
    timeout=None,
    stream=False,
    files=None,
    content=None,
    logging_obj=None,
):
    """Monkey-patched HTTPHandler.post that intercepts Braintrust calls with endpoint-specific responses."""
    # Only mock Braintrust API calls
    if isinstance(url, str) and _is_braintrust_url(url):
        verbose_logger.info(f"[BRAINTRUST MOCK] POST to {url}")
        time.sleep(_MOCK_LATENCY_SECONDS)
        # Return appropriate mock response based on endpoint
        if "/project" in url:
            # Project creation/retrieval/register endpoint
            project_name = json.get("name", "litellm") if json else "litellm"
            mock_data = {"id": f"mock-project-id-{project_name}", "name": project_name}
        elif "/project_logs" in url:
            # Log insertion endpoint
            mock_data = {"status": "success"}
        else:
            mock_data = _config.default_json_data
        return MockResponse(
            status_code=_config.default_status_code,
            json_data=mock_data,
            url=url,
            elapsed_seconds=_MOCK_LATENCY_SECONDS,
        )
    if _original_http_handler_post is not None:
        return _original_http_handler_post(
            self,
            url=url,
            data=data,
            json=json,
            params=params,
            headers=headers,
            timeout=timeout,
            stream=stream,
            files=files,
            content=content,
            logging_obj=logging_obj,
        )
    raise RuntimeError("Original HTTPHandler.post not available")

