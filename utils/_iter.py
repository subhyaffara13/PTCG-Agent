
def _iter(
    self: BaseModel,
    to_dict: bool = False,
    by_alias: bool = False,
    include: AbstractSetIntStr | MappingIntStrAny | None = None,
    exclude: AbstractSetIntStr | MappingIntStrAny | None = None,
    exclude_unset: bool = False,
    exclude_defaults: bool = False,
    exclude_none: bool = False,
) -> TupleGenerator:
    # Merge field set excludes with explicit exclude parameter with explicit overriding field set options.
    # The extra "is not None" guards are not logically necessary but optimizes performance for the simple case.
    if exclude is not None:
        exclude = _utils.ValueItems.merge(
            {k: v.exclude for k, v in self.__pydantic_fields__.items() if v.exclude is not None}, exclude
        )

    if include is not None:
        include = _utils.ValueItems.merge(dict.fromkeys(self.__pydantic_fields__, True), include, intersect=True)

    allowed_keys = _calculate_keys(self, include=include, exclude=exclude, exclude_unset=exclude_unset)  # type: ignore
    if allowed_keys is None and not (to_dict or by_alias or exclude_unset or exclude_defaults or exclude_none):
        # huge boost for plain _iter()
        yield from self.__dict__.items()
        if self.__pydantic_extra__:
            yield from self.__pydantic_extra__.items()
        return

    value_exclude = _utils.ValueItems(self, exclude) if exclude is not None else None
    value_include = _utils.ValueItems(self, include) if include is not None else None

    if self.__pydantic_extra__ is None:
        items = self.__dict__.items()
    else:
        items = list(self.__dict__.items()) + list(self.__pydantic_extra__.items())

    for field_key, v in items:
        if (allowed_keys is not None and field_key not in allowed_keys) or (exclude_none and v is None):
            continue

        if exclude_defaults:
            try:
                field = self.__pydantic_fields__[field_key]
            except KeyError:
                pass
            else:
                if not field.is_required() and field.default == v:
                    continue

        if by_alias and field_key in self.__pydantic_fields__:
            dict_key = self.__pydantic_fields__[field_key].alias or field_key
        else:
            dict_key = field_key

        if to_dict or value_include or value_exclude:
            v = _get_value(
                type(self),
                v,
                to_dict=to_dict,
                by_alias=by_alias,
                include=value_include and value_include.for_element(field_key),
                exclude=value_exclude and value_exclude.for_element(field_key),
                exclude_unset=exclude_unset,
                exclude_defaults=exclude_defaults,
                exclude_none=exclude_none,
            )
        yield dict_key, v


def _iter(tracer):
  if tracer.ndim == 0:
    raise TypeError("iteration over a 0-d array")  # same as numpy error
  else:
    n = int(tracer.shape[0])
    if any(isinstance(d, core.Tracer) for d in tracer.shape):
      return (slicing.dynamic_index_in_dim(tracer, i, keepdims=False)
              for i in range(n))
    else:
      return (slicing.index_in_dim(tracer, i, keepdims=False) for i in range(n))

