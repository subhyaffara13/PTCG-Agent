
def _player_string(player: int) -> str:
    if player == 0:
        return _X
    if player == 1:
        return _O
    return pyspiel.PlayerId(player).name.lower()


def _player_string(player: int) -> str:
    if player < 0:
        return pyspiel.PlayerId(player).name.lower()
    if player == 0:
        return PIECE_BLACK
    if player == 1:
        return PIECE_WHITE
    raise ValueError(f"Invalid player: {player}")


def _player_string(player: int) -> str:
    if player < 0:
        return pyspiel.PlayerId(player).name.lower()
    if player == 0:
        return _MAN_P0
    if player == 1:
        return _MAN_P1
    raise ValueError(f"Invalid player: {player}")


def _player_string(player: int) -> str:
    if player < 0:
        return pyspiel.PlayerId(player).name.lower()
    if player == 0:
        return _PIECE_WHITE
    if player == 1:
        return _PIECE_BLACK
    raise ValueError(f"Invalid player: {player}")


def _player_string(player: int) -> str:
    if player < 0:
        return pyspiel.PlayerId(player).name.lower()
    if player == 0:
        return "x"
    if player == 1:
        return "o"
    raise ValueError(f"Invalid player: {player}")


def _player_string(player: int) -> str:
    if player < 0:
        return pyspiel.PlayerId(player).name.lower()
    if player == 0:
        return "x"
    if player == 1:
        return "o"
    raise ValueError(f"Invalid player: {player}")


def _player_string(player: int) -> str:
    if player < 0:
        return pyspiel.PlayerId(player).name.lower()
    if player == 0:
        return "white"
    if player == 1:
        return "black"
    raise ValueError(f"Invalid player: {player}")


def _player_string(player: int) -> str:
    if player == 0:
        return "x"
    if player == 1:
        return "o"
    return pyspiel.PlayerId(player).name.lower()


def _player_string(player: int, num_players: int) -> str:
    if player < 0:
        return pyspiel.PlayerId(player).name.lower()
    if 0 <= player < num_players:
        return _PLAYER_LABELS[player]
    raise ValueError(f"Invalid player: {player}")


def _player_string(player: int) -> str:
    if player < 0:
        return pyspiel.PlayerId(player).name.lower()
    if player == 0:
        return "x"
    if player == 1:
        return "o"
    raise ValueError(f"Invalid player: {player}")

