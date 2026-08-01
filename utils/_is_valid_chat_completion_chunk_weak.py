
def _is_valid_chat_completion_chunk_weak(sse_event: ChatCompletionChunk) -> bool:
    # Although the _raw_stream is always supposed to contain only objects adhering to ChatCompletionChunk schema,
    # this is broken by the Azure OpenAI in case of Asynchronous Filter enabled.
    # An easy filter is to check for the "object" property:
    # - should be "chat.completion.chunk" for a ChatCompletionChunk;
    # - is an empty string for Asynchronous Filter events.
    return sse_event.object == "chat.completion.chunk"  # type: ignore # pylance reports this as a useless check

