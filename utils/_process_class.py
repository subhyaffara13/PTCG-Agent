
def _process_class(cls: type[M], extra_fields=None, **kwargs):
  """Transforms `cls` into a dataclass that supports kw_only fields."""
  if sys.version_info < (3, 14) and '__annotations__' not in cls.__dict__:
    cls.__annotations__ = {}

  # The original __dataclass_fields__ dicts for all base classes.  We will
  # modify these in-place before turning `cls` into a dataclass, and then
  # restore them to their original values.
  base_dataclass_fields = {}  # dict[cls, cls.__dataclass_fields__.copy()]

  # The keyword only fields from `cls` or any of its base classes.
  kw_only_fields: dict[FieldName, tuple[Annotation, Default]] = {}

  # Scan for KW_ONLY marker.
  kw_only_name = None
  for name, annotation in cls.__annotations__.items():
    if annotation is KW_ONLY:
      if kw_only_name is not None:
        raise TypeError('Multiple KW_ONLY markers')
      kw_only_name = name
    elif kw_only_name is not None:
      if not hasattr(cls, name):
        raise ValueError(
          'Keyword-only fields with no default are not supported.'
        )
      default = getattr(cls, name)
      if isinstance(default, dataclasses.Field):
        default.metadata = MappingProxyType({**default.metadata, KW_ONLY: True})
      else:
        default = field(default=default, kw_only=True)
      setattr(cls, name, default)
  if kw_only_name:
    del cls.__annotations__[kw_only_name]

  # Inject extra fields.
  if extra_fields:
    for name, annotation, default in extra_fields:
      if not (isinstance(name, str) and isinstance(default, dataclasses.Field)):
        raise ValueError(
          'Expected extra_fields to a be a list of '
          '(name, type, Field) tuples.'
        )
      setattr(cls, name, default)
      cls.__annotations__[name] = annotation

  # Extract kw_only fields from base classes' __dataclass_fields__.
  for base in reversed(cls.__mro__[1:]):
    if not dataclasses.is_dataclass(base):
      continue
    if sys.version_info < (3, 14):
      base_annotations = base.__dict__.get('__annotations__', {})
    else:
      base_annotations = inspect.get_annotations(base)

    base_dataclass_fields[base] = dict(
      getattr(base, '__dataclass_fields__', {})
    )
    for base_field in list(dataclasses.fields(base)):
      field_name = base_field.name
      if base_field.metadata.get(KW_ONLY) or field_name in kw_only_fields:
        kw_only_fields[field_name] = (
          base_annotations.get(field_name),
          base_field,
        )
        del base.__dataclass_fields__[field_name]

  # Remove any keyword-only fields from this class.
  if sys.version_info < (3, 14):
    cls_annotations = cls.__dict__['__annotations__']
  else:
    cls_annotations = cls.__annotations__
  for name, annotation in list(cls_annotations.items()):
    value = getattr(cls, name, None)
    if (
      isinstance(value, dataclasses.Field) and value.metadata.get(KW_ONLY)
    ) or name in kw_only_fields:
      del cls_annotations[name]
      kw_only_fields[name] = (annotation, value)

  # Add keyword-only fields at the end of __annotations__, in the order they
  # were found in the base classes and in this class.
  for name, (annotation, default) in kw_only_fields.items():
    setattr(cls, name, default)
    cls_annotations.pop(name, None)
    cls_annotations[name] = annotation

  create_init = '__init__' not in vars(cls) and kwargs.get('init', True)

  # Apply the dataclass transform.
  transformed_cls: type[M] = dataclasses.dataclass(cls, **kwargs)

  # Restore the base classes' __dataclass_fields__.
  for _cls, fields in base_dataclass_fields.items():
    _cls.__dataclass_fields__ = fields

  if create_init:
    dataclass_init = transformed_cls.__init__
    # use sum to count the number of init fields that are not keyword-only
    expected_num_args = sum(
      f.init and not f.metadata.get(KW_ONLY, False)
      for f in dataclasses.fields(transformed_cls)
    )

    @functools.wraps(dataclass_init)
    def init_wrapper(self, *args, **kwargs):
      num_args = len(args)
      if num_args > expected_num_args:
        # we add + 1 to each to account for `self`, matching python's
        # default error message
        raise TypeError(
          f'__init__() takes {expected_num_args + 1} positional '
          f'arguments but {num_args + 1} were given'
        )

      dataclass_init(self, *args, **kwargs)

    init_wrapper.__signature__ = inspect.signature(dataclass_init)  # type: ignore
    transformed_cls.__init__ = init_wrapper  # type: ignore[method-assign]

  # Return the transformed dataclass
  return transformed_cls

