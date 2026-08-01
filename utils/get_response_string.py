
def get_response_string(response_obj: Union[ModelResponse, ModelResponseStream]) -> str:
    # Handle Responses API streaming events
    if hasattr(response_obj, "type") and hasattr(response_obj, "response"):
        # This is a Responses API streaming event (e.g., ResponseCreatedEvent, ResponseCompletedEvent)
        # Extract text from the response object's output if available
        responses_api_response = getattr(response_obj, "response", None)
        if responses_api_response and hasattr(responses_api_response, "output"):
            output_list = responses_api_response.output
            # Use list accumulation to avoid O(n^2) string concatenation:
            # repeatedly doing `response_str += part` copies the full string each time
            # because Python strings are immutable, so total work grows with n^2.
            response_output_parts: List[str] = []
            for output_item in output_list:
                # Handle output items with content array
                if hasattr(output_item, "content"):
                    for content_part in output_item.content:
                        if hasattr(content_part, "text"):
                            response_output_parts.append(content_part.text)
                # Handle output items with direct text field
                elif hasattr(output_item, "text"):
                    response_output_parts.append(output_item.text)
            return "".join(response_output_parts)

    # Handle Responses API text delta events
    if hasattr(response_obj, "type") and hasattr(response_obj, "delta"):
        event_type = getattr(response_obj, "type", "")
        if "text.delta" in event_type or "output_text.delta" in event_type:
            delta = getattr(response_obj, "delta", "")
            return delta if isinstance(delta, str) else ""

    # Handle standard ModelResponse and ModelResponseStream
    _choices: Union[List[Choices], List[StreamingChoices]] = response_obj.choices

    # Use list accumulation to avoid O(n^2) string concatenation across choices
    response_parts: List[str] = []
    for choice in _choices:
        if isinstance(choice, Choices):
            if choice.message.content is not None:
                response_parts.append(str(choice.message.content))
        elif isinstance(choice, StreamingChoices):
            if choice.delta.content is not None:
                response_parts.append(str(choice.delta.content))

    return "".join(response_parts)

