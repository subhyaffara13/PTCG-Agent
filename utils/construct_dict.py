from typing import Any

def construct_dict(
    cls: type[T],
    data: Mapping[object, object] | Iterable[tuple[object, object]] = (),
    /,
    **kwargs: Any,
) -> T:
    self = cls.__new__(cls)
    mutable_mapping_update(self, data, **kwargs)
    return self

