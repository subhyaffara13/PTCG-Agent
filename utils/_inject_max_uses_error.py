
def _inject_max_uses_error(
    messages: List[Dict],
    executor_response: Any,
    advisor_use_block: Dict,
) -> List[Dict]:
    """
    Inject a max_uses_exceeded error tool_result so the executor continues
    without further advisor calls (mirrors Anthropic's server-side behaviour).
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
                    "content": "Advisor unavailable: max_uses limit reached. Continue without advisor guidance.",
                }
            ],
        },
    ]

