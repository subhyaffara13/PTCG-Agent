
def board_hash(hand_ids: Tuple[int, ...], board_ids: Tuple[int, ...], deck_remaining: int, turn: int) -> int:
    """Computes a deterministic hash for the current board state."""
    digest = hashlib.sha256(f"{hand_ids}|{board_ids}|{deck_remaining}|{turn}".encode()).hexdigest()
    return int(digest[:16], 16)


def board_hash(hand_ids: Tuple[int, ...], board_ids: Tuple[int, ...], deck_remaining: int, turn: int) -> int:
    """Computes a deterministic hash for the current board state."""
    digest = hashlib.sha256(f"{hand_ids}|{board_ids}|{deck_remaining}|{turn}".encode()).hexdigest()
    return int(digest[:16], 16)


def board_hash(hand_ids: Tuple[int, ...], board_ids: Tuple[int, ...], deck_remaining: int, turn: int) -> int:
    """Computes a hash for the current board state."""
    return hash((hand_ids, board_ids, deck_remaining, turn))

