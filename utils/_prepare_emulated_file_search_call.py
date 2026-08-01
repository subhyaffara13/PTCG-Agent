
def _prepare_emulated_file_search_call(
    kwargs: Dict[str, Any],
) -> Tuple[bool, Dict[str, Any]]:
    include_items: List[str] = list(kwargs.get("include") or [])
    include_search_results = "file_search_call.results" in include_items

    original_stream = kwargs.get("stream")
    updated_kwargs = kwargs
    if original_stream:
        verbose_logger.debug(
            "Streaming is not yet supported for emulated file_search. "
            "Disabling stream for this request."
        )
        updated_kwargs = {**kwargs, "stream": False}

    return include_search_results, updated_kwargs

