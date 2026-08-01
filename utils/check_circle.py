
def check_circle(mouse_pos_x, mouse_pos_y, center_x, center_y, radius):
    return (mouse_pos_x - center_x) ** 2 + (mouse_pos_y - center_y) ** 2 < radius**2

