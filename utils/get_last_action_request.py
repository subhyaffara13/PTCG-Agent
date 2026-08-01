
def get_last_action_request(event_views: Sequence[PlayerEventView], event_name: EventName) -> None | PlayerEventView:
    """Get the action request from the new player history entry view updates."""
    return next((entry for entry in event_views if entry.event_name == event_name), None)

