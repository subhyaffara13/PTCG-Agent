
def build_palette(num_labels: int) -> list[tuple[int, int, int]]:
    base = int(num_labels ** (1 / 3)) + 1
    margin = 256 // base

    # class_idx 0 is the background which is mapped to black
    color_list = [(0, 0, 0)]
    for location in range(num_labels):
        num_seq_r = location // base**2
        num_seq_g = (location % base**2) // base
        num_seq_b = location % base

        R = 255 - num_seq_r * margin
        G = 255 - num_seq_g * margin
        B = 255 - num_seq_b * margin

        color_list.append((R, G, B))

    return color_list


def build_palette(num_labels: int) -> list[tuple[int, int, int]]:
    base = int(num_labels ** (1 / 3)) + 1
    margin = 256 // base

    # class_idx 0 is the background which is mapped to black
    color_list = [(0, 0, 0)]
    for location in range(num_labels):
        num_seq_r = location // base**2
        num_seq_g = (location % base**2) // base
        num_seq_b = location % base

        R = 255 - num_seq_r * margin
        G = 255 - num_seq_g * margin
        B = 255 - num_seq_b * margin

        color_list.append((R, G, B))

    return color_list

