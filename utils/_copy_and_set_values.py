from typing import Any

def _copy_and_set_values(
    self: Model,
    values: dict[str, Any],
    fields_set: set[str],
    extra: dict[str, Any] | None = None,
    private: dict[str, Any] | None = None,
    *,
    deep: bool,  # UP006
) -> Model:
    if deep:
        # chances of having empty dict here are quite low for using smart_deepcopy
        values = deepcopy(values)
        extra = deepcopy(extra)
        private = deepcopy(private)

    cls = self.__class__
    m = cls.__new__(cls)
    _object_setattr(m, '__dict__', values)
    _object_setattr(m, '__pydantic_extra__', extra)
    _object_setattr(m, '__pydantic_fields_set__', fields_set)
    _object_setattr(m, '__pydantic_private__', private)

    return m

