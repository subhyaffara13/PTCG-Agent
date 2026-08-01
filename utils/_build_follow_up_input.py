
def _build_follow_up_input(
    input: Any,
    first_response: ResponsesAPIResponse,
    tool_results: List[Dict[str, Any]],
) -> List[Any]:
    """Assemble the follow-up call input: original messages + first-response output + tool results.

    Including all output items (text blocks, reasoning, non-file-search calls) ensures providers
    like Anthropic that emit text before the tool call have complete conversation context.
    Serializes Pydantic model instances to plain dicts so the transformation layer can call .get().
    """
    original_input_items = (
        list(input)
        if isinstance(input, (list, tuple))
        else [{"role": "user", "content": str(input)}]
    )
    first_response_output_items: List[Any] = []
    for _item in first_response.output:
        if isinstance(_item, dict):
            first_response_output_items.append(_item)
        elif hasattr(_item, "model_dump"):
            first_response_output_items.append(_item.model_dump(exclude_none=True))  # type: ignore[union-attr]
        else:
            first_response_output_items.append(_item)

    return original_input_items + first_response_output_items + tool_results

