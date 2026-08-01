
def draw_text_line(text, y=0):
    """
    Draws a line of text onto the display surface
    The text will be centered horizontally at the given y position
    The text's height is added to y and returned to the caller
    """
    screen = pg.display.get_surface()
    surf = font.render(text, 1, (255, 255, 255))
    y += surf.get_height()
    x = (screen.get_width() - surf.get_width()) / 2
    screen.blit(surf, (x, y))
    return y

