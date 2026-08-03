from typing import Any

def make_wrapped_dispatch(bus, g_logger):
    original_dispatch = bus.dispatch
    def wrapped_dispatch(event_name: str, packet: Any) -> Any:
        state_before = getattr(packet, "board_summary", {}) if hasattr(packet, "board_summary") else {}
        response = original_dispatch(event_name, packet)
        state_after = {"status": "dispatched", "response": str(response)}
        g_logger.log_action(turn=getattr(packet, "turn", 0) if hasattr(packet, "turn") else 1, agent_called=bus.delegation_map.get(event_name, "unknown"), action_taken=event_name, game_state_before=state_before, game_state_after=state_after)
        return response
    bus.dispatch = wrapped_dispatch

