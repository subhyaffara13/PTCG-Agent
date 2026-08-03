import re
from typing import Any

def _reconstruct_move_history(observation: Mapping[str, Any]) -> list[str]:
    """Rebuild the full-game move history from the serialized pyspiel state.

    Used only when the proxy state dict didn't surface ``move_history`` (e.g.
    older replays). Clobber has no chance phase, so play actions alternate
    starting with player 0.
    """
    serialized = observation.get("serializedGameAndState", "")
    if not serialized:
        return []
    _, state = pyspiel.deserialize_game_and_state(serialized)
    return [
        state.action_to_string(idx % 2, action)
        for idx, action in enumerate(state.history())
    ]


def _reconstruct_move_history(observation: Mapping[str, Any]) -> list[str]:
    """Reconstruct the list of all played moves with player labels from deserialized state."""
    serialized = observation.get("serializedGameAndState", "")
    if not serialized:
        return []
    try:
        game, state = pyspiel.deserialize_game_and_state(serialized)
        temp_state = game.new_initial_state()
        history_strings = []
        for action in state.history():
            player = temp_state.current_player()
            action_str = temp_state.action_to_string(player, action)
            symbol = "x" if player == 0 else "o"

            m_board = re.match(r"^choose local board (\d)", action_str, re.IGNORECASE)
            if m_board:
                board_idx = m_board.group(1)
                history_strings.append(f"Player {player} ({symbol}): chose board {board_idx}")
            else:
                m_cell = re.match(r"^local board (\d):\s*([xo])\((\d),(\d)\)", action_str, re.IGNORECASE)
                if m_cell:
                    board_idx, sym, r, c = m_cell.groups()
                    cell_idx = int(r) * 3 + int(c)
                    history_strings.append(
                        f"Player {player} ({symbol}): board {board_idx} cell ({r},{c}) [idx {cell_idx}]"
                    )
                else:
                    history_strings.append(f"Player {player} ({symbol}): {action_str}")
            temp_state.apply_action(action)
        return history_strings
    except Exception:
        return []

