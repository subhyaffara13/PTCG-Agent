
def slice_and_offset(crd: tuple[object, ...], layout: Layout) -> tuple[Layout, int]:
    return (
        Layout(slice_(crd, layout.shape), slice_(crd, layout.stride)),
        crd2idx(crd, layout.shape, layout.stride),  # type: ignore[arg-type]
    )

