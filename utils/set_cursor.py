
def set_cursor(*args):
    """set_cursor(pygame.cursors.Cursor OR args for a pygame.cursors.Cursor) -> None
    set the mouse cursor to a new cursor"""
    cursor = Cursor(*args)
    pygame.mouse._set_cursor(**{cursor.type: cursor.data})

