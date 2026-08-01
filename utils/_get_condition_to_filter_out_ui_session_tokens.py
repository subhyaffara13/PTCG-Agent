
def _get_condition_to_filter_out_ui_session_tokens() -> Dict[str, Any]:
    """
    Condition to filter out UI session tokens
    """
    return {
        "OR": [
            {"team_id": None},  # Include records where team_id is null
            {
                "team_id": {"not": UI_SESSION_TOKEN_TEAM_ID}
            },  # Include records where team_id != UI_SESSION_TOKEN_TEAM_ID
        ]
    }

