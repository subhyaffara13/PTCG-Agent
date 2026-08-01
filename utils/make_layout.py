
def make_layout(*layouts: Layout | tuple[Layout, ...]) -> Layout:
    if len(layouts) == 1 and not is_layout(layouts[0]):
        layouts = layouts[0]

    shape, stride = zip(*((a.shape, a.stride) for a in layouts))  # type: ignore[union-attr]
    return Layout(shape, stride)

