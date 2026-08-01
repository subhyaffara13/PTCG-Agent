
def _serialize_streaming_chunk(chunk: BaseModel) -> Union[str, bytes]:
    if isinstance(chunk, ModelResponseStream):
        serialized_chunk = _fast_serialize_simple_model_response_stream(chunk)
        if serialized_chunk is not None:
            return serialized_chunk

    return chunk.model_dump_json(exclude_none=True, exclude_unset=True)

