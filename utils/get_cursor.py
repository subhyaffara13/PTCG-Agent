
def get_cursor():
    """get_cursor() -> pygame.cursors.Cursor
    get the current mouse cursor"""
    return Cursor(*pygame.mouse._get_cursor())

