
def _inject_advisor_turn(
    messages: List[Dict],
    executor_response: Any,
    advisor_use_block: Dict,
    advisor_text: str,
) -> List[Dict]:
    """
    Append the executor's response (as an assistant turn) and the advisor
    result (as a user tool_result turn) so the executor can continue.
    """
    executor_content = (
        executor_response.get("content") if isinstance(executor_response, dict) else []
    ) or []
    tool_use_id = advisor_use_block.get("id", "")
    return [
        *messages,
        {"role": "assistant", "content": executor_content},
        {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": tool_use_id,
                    "content": advisor_text,
                }
            ],
        },
    ]

