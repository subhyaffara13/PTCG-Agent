
def is_claude_code_user_agent(user_agent: str) -> bool:
    """Claude Code identifies itself as ``claude-cli/<version> ...``; the IDE
    extensions and the Agent SDK run through the same CLI and share that prefix."""
    return user_agent.startswith("claude-cli/")

