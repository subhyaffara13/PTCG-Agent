
def convert_generic_chunk_to_model_response_stream(
    chunk: GChunk,
) -> ModelResponseStream:
    from litellm.types.utils import Delta

    model_response_stream = ModelResponseStream(
        id=str(uuid.uuid4()),
        model="",
        choices=[
            StreamingChoices(
                index=chunk.get("index", 0),
                delta=Delta(
                    content=chunk["text"],
                    tool_calls=chunk.get("tool_use", None),
                ),
            )
        ],
        finish_reason=chunk["finish_reason"] if chunk["is_finished"] else None,
    )

    if "usage" in chunk and chunk["usage"] is not None:
        setattr(model_response_stream, "usage", chunk["usage"])

    return model_response_stream

