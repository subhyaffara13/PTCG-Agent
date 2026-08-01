
def _get_value(x):
    # item is significantly faster than a cpu tensor in eager mode
    if not torch.jit.is_scripting() and torch.compiler.is_compiling():
        return x
    else:
        return x.item() if isinstance(x, torch.Tensor) else x


def _get_value(
    cls: type[BaseModel],
    v: Any,
    to_dict: bool,
    by_alias: bool,
    include: AbstractSetIntStr | MappingIntStrAny | None,
    exclude: AbstractSetIntStr | MappingIntStrAny | None,
    exclude_unset: bool,
    exclude_defaults: bool,
    exclude_none: bool,
) -> Any:
    from .. import BaseModel

    if isinstance(v, BaseModel):
        if to_dict:
            return v.model_dump(
                by_alias=by_alias,
                exclude_unset=exclude_unset,
                exclude_defaults=exclude_defaults,
                include=include,  # type: ignore
                exclude=exclude,  # type: ignore
                exclude_none=exclude_none,
            )
        else:
            return v.copy(include=include, exclude=exclude)

    value_exclude = _utils.ValueItems(v, exclude) if exclude else None
    value_include = _utils.ValueItems(v, include) if include else None

    if isinstance(v, dict):
        return {
            k_: _get_value(
                cls,
                v_,
                to_dict=to_dict,
                by_alias=by_alias,
                exclude_unset=exclude_unset,
                exclude_defaults=exclude_defaults,
                include=value_include and value_include.for_element(k_),
                exclude=value_exclude and value_exclude.for_element(k_),
                exclude_none=exclude_none,
            )
            for k_, v_ in v.items()
            if (not value_exclude or not value_exclude.is_excluded(k_))
            and (not value_include or value_include.is_included(k_))
        }

    elif _utils.sequence_like(v):
        seq_args = (
            _get_value(
                cls,
                v_,
                to_dict=to_dict,
                by_alias=by_alias,
                exclude_unset=exclude_unset,
                exclude_defaults=exclude_defaults,
                include=value_include and value_include.for_element(i),
                exclude=value_exclude and value_exclude.for_element(i),
                exclude_none=exclude_none,
            )
            for i, v_ in enumerate(v)
            if (not value_exclude or not value_exclude.is_excluded(i))
            and (not value_include or value_include.is_included(i))
        )

        return v.__class__(*seq_args) if _typing_extra.is_namedtuple(v.__class__) else v.__class__(seq_args)

    elif isinstance(v, Enum) and getattr(cls.model_config, 'use_enum_values', False):
        return v.value

    else:
        return v


def _get_value(obj: Any, key: str) -> Any:
    if isinstance(obj, dict):
        return obj.get(key)
    return getattr(obj, key, None)

