
def _view_has_unbacked_input(
    a: torch.Tensor, shape: ShapeType | tuple[ShapeType]
) -> bool:
    from torch.fx.experimental.symbolic_shapes import has_guarding_hint

    shape = utils.extract_shape_from_varargs(shape, validate=False)

    return (
        any(not has_guarding_hint(s) for s in a.size())
        or any(not has_guarding_hint(s) for s in a.stride())
        or any(not has_guarding_hint(s) for s in shape)
    )

