
def _convert_initial_chunk_into_snapshot(chunk: ChatCompletionChunk) -> ParsedChatCompletionSnapshot:
    data = chunk.to_dict()
    choices = cast("list[object]", data["choices"])

    for choice in chunk.choices:
        choices[choice.index] = {
            **choice.model_dump(exclude_unset=True, exclude={"delta"}),
            "message": choice.delta.to_dict(),
        }

    return cast(
        ParsedChatCompletionSnapshot,
        construct_type(
            type_=ParsedChatCompletionSnapshot,
            value={
                "system_fingerprint": None,
                **data,
                "object": "chat.completion",
            },
        ),
    )

