from typing import Optional

def memref(
    *shape,
    element_type: Type = None,
    memory_space: Optional[int] = None,
    layout: Optional[StridedLayoutAttr] = None,
):
    if memory_space is not None:
        memory_space = Attribute.parse(str(memory_space))
    if not shape or (len(shape) == 1 and isinstance(shape[-1], Type)):
        return _shaped(
            *shape,
            element_type=element_type,
            type_constructor=partial(UnrankedMemRefType.get, memory_space=memory_space),
        )
    return _shaped(
        *shape,
        element_type=element_type,
        type_constructor=partial(
            MemRefType.get, memory_space=memory_space, layout=layout
        ),
    )

