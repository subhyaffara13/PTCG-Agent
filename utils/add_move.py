
def add_move(move):
    """Add an item to six.moves."""
    setattr(_MovedItems, move.name, move)

