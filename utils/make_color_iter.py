
def make_color_iter(color_map, num_rows, num_cols):
    num_colors = num_rows * num_cols
    for idx in range(num_colors):
        yield color_map(idx)


def make_color_iter(color_map, num_rows, num_cols):
  num_colors = num_rows * num_cols
  color_values = np.linspace(0, 1, num_colors)
  idx = 0
  for _ in range(num_colors):
    yield color_map(color_values[idx])
    idx = (idx + num_colors // 2 + bool(num_colors % 2 == 0)) % num_colors

