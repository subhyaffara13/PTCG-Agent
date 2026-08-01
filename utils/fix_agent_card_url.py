
def fix_agent_card_url(agent_card: "AgentCard", base_url: str) -> "AgentCard":
    """
    Fix the agent card URL if it contains a localhost/internal address.

    Many A2A agents are deployed with agent cards that contain internal URLs
    like "http://0.0.0.0:8001/" or "http://localhost:8000/". This function
    replaces such URLs with the provided base_url.

    Args:
        agent_card: The agent card to fix
        base_url: The base URL to use as replacement

    Returns:
        The agent card with the URL fixed if necessary
    """
    card_url = getattr(agent_card, "url", None)

    if card_url and is_localhost_or_internal_url(card_url):
        # Normalize base_url to ensure it ends with /
        fixed_url = base_url.rstrip("/") + "/"
        agent_card.url = fixed_url

    return agent_card

