
def pretty_repr_top_level(obj: Any, *, force: bool = True) -> str:
  """Pretty `repr(obj)` for nested list, dict, dataclasses,...

  This version do not use `@reprlib.recursive_repr()` to avoid bug when used
  inside `__repr__`:

  ```python
  @dataclasses.dataclass  # Or @attrs.frozen,...
  class A:

    def __repr__(self):
      return epy.pretty_repr_top_level(self)

  print(repr(A()))
  ```

  Args:
    obj: Object to display
    force: Force the pretty_repr, even if the object has a custom `__repr__`.
      This is useful when the `__repr__` implementation itself want to call
      `pretty_repr(self)`.

  Returns:
    Repr
  """
  # TODO(epot): Should still somehow register `self` with the `recursive_repr`,
  # should support both:
  # pretty_repr(a) == A(recursive=...)
  # a.__repr__() == A(recursive=...)

  if isinstance(obj, str):
    return repr(obj)
  elif py_utils.is_namedtuple(obj):
    # TODO(epot): Could check if obj has custom `__repr__`
    return Lines.make_block(
        header=obj.__class__.__name__,
        content={
            field_name: getattr(obj, field_name)
            for field_name in type(obj)._fields
        },
    )
  elif type(obj) in (list, tuple):  # Skip sub-class as could have custom repr
    lines = Lines.make_block(
        content=obj,
        braces='[' if isinstance(obj, list) else '(',
    )
    # Singleton tuple have a trailing `,`
    if isinstance(obj, tuple) and len(obj) == 1:
      lines = lines.removesuffix(')') + ',)'
    return lines
  elif type(obj) is dict:  # pylint: disable=unidiomatic-typecheck
    return Lines.make_block(
        content={pretty_repr(k): v for k, v in obj.items()},
        braces='{',
        equal=': ',
    )
  elif _is_dict_subclass(obj, force=force):  # pylint: disable=unidiomatic-typecheck
    return Lines.make_block(
        header=obj.__class__.__name__,
        content={pretty_repr(k): v for k, v in obj.items()},
        braces=('({', '})'),
        equal=': ',
    )
  elif _is_datclass(obj, force=force):
    all_fields = dataclasses.fields(obj)

    return Lines.make_block(
        header=obj.__class__.__name__,
        content={
            field.name: getattr(obj, field.name)
            for field in all_fields
            if field.repr
        },
    )
  elif _is_pydantic(obj, force=force):
    return Lines.make_block(
        header=obj.__class__.__name__,
        content={
            field_name: getattr(obj, field_name)
            for field_name, field_info in obj.model_fields.items()
            if field_info.repr
        },
    )
  elif _is_attr(obj, force=force):
    import attr  # pylint: disable=g-import-not-at-top  # pytype: disable=import-error

    all_fields = attr.fields_dict(type(obj))

    return Lines.make_block(
        header=obj.__class__.__name__,
        content={
            field.name: getattr(obj, field.name)
            for field in all_fields.values()
            if field.repr
        },
    )
  elif _is_immutabledict(obj, force=force):
    return Lines.make_block(
        header=obj.__class__.__name__,
        content={pretty_repr(k): v for k, v in obj.items()},
        braces=('({', '})'),
        equal=': ',
    )
  elif _is_userdict(obj, force=force):
    return Lines.make_block(
        header=obj.__class__.__name__,
        content={pretty_repr(k): v for k, v in obj.items()},
        braces=('({', '})'),
        equal=': ',
    )
  # TODO(epot): When the new fiddle version is release on PyPI, this
  # code could be activated (with the matching test).
  elif _is_fiddle(obj):
    import fiddle  # pylint: disable=g-import-not-at-top  # pytype: disable=import-error

    cls_name = type(obj).__name__
    formatted_fn_or_cls = obj._fn_or_cls_name_repr()  # pylint: disable=protected-access

    formatted_params = []
    for name, tags, value in obj._params_name_tags_and_value():  # pylint: disable=protected-access
      if not tags and value is fiddle.NO_VALUE:
        continue

      param_str = str(name)
      if tags:
        param_str += f"[{', '.join(sorted(str(tag) for tag in tags))}]"
      if value is not fiddle.NO_VALUE:
        param_str += f'={pretty_repr(value)}'
      formatted_params.append(_Repr(param_str))

    return Lines.make_block(
        header=f'<{cls_name}[{formatted_fn_or_cls}',
        content=formatted_params,
        braces=('(', ')]>'),
    )
  elif force:
    raise ValueError(
        '`epy.pretty_repr_top_level` should only be called on `@dataclasses`,'
        f' `attrs`,... objects. Got {type(obj)!r}'
    )
  else:
    return repr(obj)

