
def from_components(translation: Array, quat: Array) -> Array:
    return compose_transforms(from_translation(translation), from_rotation(quat))

