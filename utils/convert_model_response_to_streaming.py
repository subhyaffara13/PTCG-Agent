from typing import List

def convert_model_response_to_streaming(
    model_response: ModelResponse,
) -> ModelResponseStream:
    """
    Convert a ModelResponse to ModelResponseStream.

    This function transforms a standard completion response into a streaming chunk format
    by converting 'message' fields to 'delta' fields.

    Args:
        model_response: The ModelResponse to convert

    Returns:
        ModelResponseStream: A streaming chunk version of the response

    Raises:
        ValueError: If the conversion fails
    """
    try:
        streaming_choices: List[StreamingChoices] = []
        for choice in model_response.choices:
            streaming_choices.append(
                StreamingChoices(
                    index=choice.index,
                    delta=Delta(
                        **cast(Choices, choice).message.model_dump(),
                    ),
                    finish_reason=choice.finish_reason,
                )
            )
        processed_chunk = ModelResponseStream(
            id=model_response.id,
            object="chat.completion.chunk",
            created=model_response.created,
            model=model_response.model,
            choices=streaming_choices,
        )
        # Carry usage onto the streaming chunk so fake-streamed responses
        # (e.g. Vertex AI Gemma :predict) still report token counts.
        usage = getattr(model_response, "usage", None)
        if usage is not None:
            setattr(processed_chunk, "usage", usage)
        return processed_chunk
    except Exception as e:
        raise ValueError(
            f"Failed to convert ModelResponse to ModelResponseStream: {model_response}. Error: {e}"
        )

