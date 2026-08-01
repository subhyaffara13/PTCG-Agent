
def original_obs_shape(screen_width, screen_height, kernel_window_length=2):
    return (
        int(screen_height * 2 / kernel_window_length),
        int(screen_width * 2 / (kernel_window_length)),
        1,
    )

