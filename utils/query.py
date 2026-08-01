
def query(key):
    """Ask for a value of the given configuration item. """
    return _current_config.get(key.upper(), None)


def query(
    model: str,
    messages: List[Any],
    retrieval_config: Dict[str, Any],
    rerank: Optional[Dict[str, Any]] = None,
    stream: bool = False,
    **kwargs,
) -> Union[ModelResponse, Coroutine[Any, Any, ModelResponse]]:
    """
    Query a RAG pipeline.
    """
    local_vars = locals()
    try:
        _is_async = kwargs.pop("aquery", False) is True

        if _is_async:
            return _execute_query_pipeline(
                model=model,
                messages=messages,
                retrieval_config=retrieval_config,
                rerank=rerank,
                stream=stream,
                **kwargs,
            )
        else:
            return asyncio.get_event_loop().run_until_complete(
                _execute_query_pipeline(
                    model=model,
                    messages=messages,
                    retrieval_config=retrieval_config,
                    rerank=rerank,
                    stream=stream,
                    **kwargs,
                )
            )
    except Exception as e:
        raise litellm.exception_type(
            model=model,
            custom_llm_provider=retrieval_config.get("custom_llm_provider"),
            original_exception=e,
            completion_kwargs=local_vars,
            extra_kwargs=kwargs,
        )

