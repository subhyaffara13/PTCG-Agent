
def _build_system_prompt(is_admin: bool) -> str:
    """Build role-appropriate system prompt with today's date."""
    tool_desc = _TOOL_DESCRIPTIONS_ADMIN if is_admin else _TOOL_DESCRIPTIONS_BASE
    return (
        f"{_SYSTEM_PROMPT_BASE}\n\n{tool_desc}"
        f"Today's date: {date.today().isoformat()}"
    )

