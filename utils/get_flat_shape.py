
def get_flat_shape(width, height, kernel_window_length=2):
    return int(width * height / (kernel_window_length * kernel_window_length))

