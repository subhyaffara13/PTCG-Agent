
def _draw_all_if_interactive() -> None:
    if matplotlib.is_interactive():
        draw_all()

