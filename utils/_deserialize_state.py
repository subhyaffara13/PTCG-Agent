
def _deserialize_state(observation: Mapping[str, Any]) -> pyspiel.State | None:
    serialized = observation.get("serializedGameAndState", "")
    if not serialized:
        return None
    _, state = pyspiel.deserialize_game_and_state(serialized)
    return state

