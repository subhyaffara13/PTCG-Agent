
def validate_and_fix_thinking_param(
    thinking: Optional["AnthropicThinkingParam"],
) -> Optional["AnthropicThinkingParam"]:
    """
    Normalizes camelCase keys in the thinking param to snake_case.
    Handles clients that send budgetTokens instead of budget_tokens.
    """
    if thinking is None or not isinstance(thinking, dict):
        return thinking
    normalized = dict(thinking)
    if "budgetTokens" in normalized and "budget_tokens" not in normalized:
        normalized["budget_tokens"] = normalized.pop("budgetTokens")
    elif "budgetTokens" in normalized and "budget_tokens" in normalized:
        normalized.pop("budgetTokens")
    return cast("AnthropicThinkingParam", normalized)

