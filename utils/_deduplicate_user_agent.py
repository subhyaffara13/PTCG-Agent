
def _deduplicate_user_agent(user_agent: str) -> str:
    """Deduplicate redundant information in the generated user-agent."""
    # Split around ";" > Strip whitespaces > Store as dict keys (ensure unicity) > format back as string
    # Order is implicitly preserved by dictionary structure (see https://stackoverflow.com/a/53657523).
    return "; ".join({key.strip(): None for key in user_agent.split(";")}.keys())

