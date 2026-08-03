import json
from typing import Any

def _inject_memory_context(observation: Mapping[str, Any]) -> str:
    """Build memory-context string from observation history fields.

    Note: history is already trimmed to ``memory_window_size`` at save time
    by ``memory.save_game_to_history``, so no additional slicing is needed here.
    """
    parts: list[str] = []

    history = observation.get("history")
    if history:
        parts.append("\nHere is the history of past games in this session:\n")
        parts.append(json.dumps(history, indent=2))
        parts.append(
            "\n\nNote: The board is reshuffled each game — the same word may "
            "appear with a different role (blue/yellow/neutral/trap) than it "
            "had in any past game.\n\n",
        )

    current_game_turns = observation.get("current_game_turns")
    if current_game_turns:
        parts.append("Clues and guesses in this game so far:\n")
        parts.append(json.dumps(current_game_turns, indent=2))
        parts.append("\n\n")

    return "".join(parts)

