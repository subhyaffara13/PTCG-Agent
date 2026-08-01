
def interpolate_color(color1, color2, ratio):
    return tuple(interpolate(color1[i], color2[i], ratio) for i in range(3))

