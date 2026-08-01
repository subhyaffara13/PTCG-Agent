
def apply_proxy_header_overrides(
    project_name: str,
    tags: List[str],
    thread_id: Optional[str],
    proxy_headers: Dict[str, Any],
) -> Tuple[str, List[str], Optional[str]]:
    """
    Apply overrides from proxy request headers (opik_* prefix).

    Args:
        project_name: Current project name
        tags: Current tags list
        thread_id: Current thread ID
        proxy_headers: HTTP headers from proxy request

    Returns:
        Tuple of (project_name, tags, thread_id) with overrides applied
    """
    for key, value in proxy_headers.items():
        if not key.startswith("opik_") or not value:
            continue

        param_key = key.replace("opik_", "", 1)

        if param_key == "project_name":
            project_name = value
        elif param_key == "thread_id":
            thread_id = value
        elif param_key == "tags":
            try:
                parsed_tags = json.loads(value)
                if isinstance(parsed_tags, list):
                    tags.extend(parsed_tags)
            except (json.JSONDecodeError, TypeError):
                _logging.verbose_logger.warning(
                    f"Failed to parse tags from header: {value}"
                )

    return project_name, tags, thread_id

