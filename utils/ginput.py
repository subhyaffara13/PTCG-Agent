
def ginput(
    n: int = 1,
    timeout: float = 30,
    show_clicks: bool = True,
    mouse_add: MouseButton = MouseButton.LEFT,
    mouse_pop: MouseButton = MouseButton.RIGHT,
    mouse_stop: MouseButton = MouseButton.MIDDLE,
) -> list[tuple[int, int]]:
    return gcf().ginput(
        n=n,
        timeout=timeout,
        show_clicks=show_clicks,
        mouse_add=mouse_add,
        mouse_pop=mouse_pop,
        mouse_stop=mouse_stop,
    )

