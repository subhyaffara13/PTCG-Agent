
def _flatten_space_box(space: Box) -> Box:
    return Box(space.low.flatten(), space.high.flatten(), dtype=space.dtype)


def _flatten_space_box(space: Box) -> Box:
    return Box(space.low.flatten(), space.high.flatten(), dtype=space.dtype)

