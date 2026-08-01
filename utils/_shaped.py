
def _shaped(*shape, element_type: Type = None, type_constructor=None):
    if type_constructor is None:
        raise ValueError("shaped is an abstract base class - cannot be constructed.")
    if (element_type is None and shape and not isinstance(shape[-1], Type)) or (
        shape and isinstance(shape[-1], Type) and element_type is not None
    ):
        raise ValueError(
            f"Either element_type must be provided explicitly XOR last arg to tensor type constructor must be the element type."
        )
    if element_type is not None:
        type = element_type
        sizes = shape
    else:
        type = shape[-1]
        sizes = shape[:-1]
    if sizes:
        return type_constructor(sizes, type)
    else:
        return type_constructor(type)

