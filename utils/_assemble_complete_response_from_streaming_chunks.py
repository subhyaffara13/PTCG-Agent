
def _assemble_complete_response_from_streaming_chunks(
    result: Union[ModelResponse, TextCompletionResponse, ModelResponseStream],
    start_time: datetime,
    end_time: datetime,
    request_kwargs: dict,
    streaming_chunks: List[Any],
    is_async: bool,
):
    """
    Assemble a complete response from a streaming chunks

    - assemble a complete streaming response if result.choices[0].finish_reason is not None
    - else append the chunk to the streaming_chunks


    Args:
        result: ModelResponse
        start_time: datetime
        end_time: datetime
        request_kwargs: dict
        streaming_chunks: List[Any]
        is_async: bool

    Returns:
        Optional[Union[ModelResponse, TextCompletionResponse]]: Complete streaming response

    """
    complete_streaming_response: Optional[
        Union[ModelResponse, TextCompletionResponse]
    ] = None

    if isinstance(result, ModelResponse):
        return result

    if result.choices[0].finish_reason is not None:  # if it's the last chunk
        streaming_chunks.append(result)
        try:
            complete_streaming_response = litellm.stream_chunk_builder(
                chunks=streaming_chunks,
                messages=request_kwargs.get("messages", None),
                start_time=start_time,
                end_time=end_time,
            )
        except Exception as e:
            log_message = (
                "Error occurred building stream chunk in {} success logging: {}".format(
                    "async" if is_async else "sync", str(e)
                )
            )
            verbose_logger.exception(log_message)
            complete_streaming_response = None
    else:
        streaming_chunks.append(result)
    return complete_streaming_response

