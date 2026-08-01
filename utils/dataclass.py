
def dataclass(clz: _T, **kwargs) -> _T:
  ...


def dataclass(**kwargs) -> Callable[[_T], _T]:
  ...


def dataclass(
    clz: _T | None = None,
    **kwargs,
) -> _T | Callable[[_T], _T]:
  """Create a class which can be passed to functional transformations.

  .. note::
    Inherit from ``PyTreeNode`` instead to avoid type checking issues when
    using PyType.

  Jax transformations such as ``jax.jit`` and ``jax.grad`` require objects that are
  immutable and can be mapped over using the ``jax.tree_util`` methods.
  The ``dataclass`` decorator makes it easy to define custom classes that can be
  passed safely to Jax. Define JAX data as normal attribute fields, and use
  ``pytree_node=False`` to define static metadata.

  See example::

    >>> from flax import struct
    >>> import jax
    >>> from typing import Any, Callable

    >>> @struct.dataclass
    ... class Model:
    ...   params: Any
    ...   # use pytree_node=False to indicate an attribute should not be touched
    ...   # by Jax transformations.
    ...   apply_fn: Callable = struct.field(pytree_node=False)

    ...   def __apply__(self, *args):
    ...     return self.apply_fn(*args)

    >>> params = {}
    >>> params_b = {}
    >>> apply_fn = lambda v, x: x
    >>> model = Model(params, apply_fn)

    >>> # model.params = params_b  # Model is immutable. This will raise an error.
    >>> model_b = model.replace(params=params_b)  # Use the replace method instead.

    >>> # This class can now be used safely in Jax to compute gradients w.r.t. the
    >>> # parameters.
    >>> model = Model(params, apply_fn)
    >>> loss_fn = lambda model: 3.
    >>> model_grad = jax.grad(loss_fn)(model)

  Note that dataclasses have an auto-generated ``__init__`` where
  the arguments of the constructor and the attributes of the created
  instance match 1:1. If you desire a "smart constructor", for example to
  optionally derive some of the attributes from others,
  make an additional static or class method. Consider the following example::

    >>> @struct.dataclass
    ... class DirectionAndScaleKernel:
    ...   direction: jax.Array
    ...   scale: jax.Array

    ...   @classmethod
    ...   def create(cls, kernel):
    ...     scale = jax.numpy.linalg.norm(kernel, axis=0, keepdims=True)
    ...     direction = direction / scale
    ...     return cls(direction, scale)

  Args:
    clz: the class that will be transformed by the decorator.
    **kwargs: arguments to pass to the dataclass constructor.

  Returns:
    The new class.
  """
  # Support passing arguments to the decorator (e.g. @dataclass(kw_only=True))
  if clz is None:
    return functools.partial(dataclass, **kwargs)  # type: ignore[bad-return-type]

  # check if already a flax dataclass
  if '_flax_dataclass' in clz.__dict__:
    return clz

  if 'frozen' not in kwargs.keys():
    kwargs['frozen'] = True
  data_clz = dataclasses.dataclass(**kwargs)(clz)  # type: ignore
  meta_fields = []
  data_fields = []
  for field_info in dataclasses.fields(data_clz):
    is_pytree_node = field_info.metadata.get('pytree_node', True)
    if is_pytree_node:
      data_fields.append(field_info.name)
    else:
      meta_fields.append(field_info.name)

  def replace(self, **updates):
    """Returns a new object replacing the specified fields with new values."""
    return dataclasses.replace(self, **updates)

  data_clz.replace = replace

  jax.tree_util.register_dataclass(data_clz, data_fields, meta_fields)

  def to_state_dict(x):
    state_dict = {
      name: serialization.to_state_dict(getattr(x, name))
      for name in data_fields
    }
    return state_dict

  def from_state_dict(x, state):
    """Restore the state of a data class."""
    state = state.copy()  # copy the state so we can pop the restored fields.
    updates = {}
    for name in data_fields:
      if name not in state:
        raise ValueError(
          f'Missing field {name} in state dict while restoring'
          f' an instance of {clz.__name__},'
          f' at path {serialization.current_path()}'
        )
      value = getattr(x, name)
      value_state = state.pop(name)
      updates[name] = serialization.from_state_dict(
        value, value_state, name=name
      )
    if state:
      names = ','.join(state.keys())
      raise ValueError(
        f'Unknown field(s) "{names}" in state dict while'
        f' restoring an instance of {clz.__name__}'
        f' at path {serialization.current_path()}'
      )
    return x.replace(**updates)

  serialization.register_serialization_state(
    data_clz, to_state_dict, from_state_dict
  )

  # add a _flax_dataclass flag to distinguish from regular dataclasses
  data_clz._flax_dataclass = True  # type: ignore[attr-defined]

  return data_clz  # type: ignore


def dataclass(
    _cls: type[_T] | None = None,
    *,
    init: Literal[False] = False,
    repr: bool = True,
    eq: bool = True,
    order: bool = False,
    unsafe_hash: bool = False,
    frozen: bool | None = None,
    config: ConfigDict | type[object] | None = None,
    validate_on_init: bool | None = None,
    kw_only: bool = False,
    slots: bool = False,
) -> Callable[[type[_T]], type[PydanticDataclass]] | type[PydanticDataclass]:
    """!!! abstract "Usage Documentation"
        [`dataclasses`](../concepts/dataclasses.md)

    A decorator used to create a Pydantic-enhanced dataclass, similar to the standard Python `dataclass`,
    but with added validation.

    This function should be used similarly to `dataclasses.dataclass`.

    Args:
        _cls: The target `dataclass`.
        init: Included for signature compatibility with `dataclasses.dataclass`, and is passed through to
            `dataclasses.dataclass` when appropriate. If specified, must be set to `False`, as pydantic inserts its
            own  `__init__` function.
        repr: A boolean indicating whether to include the field in the `__repr__` output.
        eq: Determines if a `__eq__` method should be generated for the class.
        order: Determines if comparison magic methods should be generated, such as `__lt__`, but not `__eq__`.
        unsafe_hash: Determines if a `__hash__` method should be included in the class, as in `dataclasses.dataclass`.
        frozen: Determines if the generated class should be a 'frozen' `dataclass`, which does not allow its
            attributes to be modified after it has been initialized. If not set, the value from the provided `config` argument will be used (and will default to `False` otherwise).
        config: The Pydantic config to use for the `dataclass`.
        validate_on_init: A deprecated parameter included for backwards compatibility; in V2, all Pydantic dataclasses
            are validated on init.
        kw_only: Determines if `__init__` method parameters must be specified by keyword only. Defaults to `False`.
        slots: Determines if the generated class should be a 'slots' `dataclass`, which does not allow the addition of
            new attributes after instantiation.

    Returns:
        A decorator that accepts a class as its argument and returns a Pydantic `dataclass`.

    Raises:
        AssertionError: Raised if `init` is not `False` or `validate_on_init` is `False`.
    """
    assert init is False, 'pydantic.dataclasses.dataclass only supports init=False'
    assert validate_on_init is not False, 'validate_on_init=False is no longer supported'

    if sys.version_info >= (3, 10):
        kwargs = {'kw_only': kw_only, 'slots': slots}
    else:
        kwargs = {}

    def create_dataclass(cls: type[Any]) -> type[PydanticDataclass]:
        """Create a Pydantic dataclass from a regular dataclass.

        Args:
            cls: The class to create the Pydantic dataclass from.

        Returns:
            A Pydantic dataclass.
        """
        from ._internal._utils import is_model_class

        if is_model_class(cls):
            raise PydanticUserError(
                f'Cannot create a Pydantic dataclass from {cls.__name__} as it is already a Pydantic model',
                code='dataclass-on-model',
            )

        original_cls = cls

        # we warn on conflicting config specifications, but only if the class doesn't have a dataclass base
        # because a dataclass base might provide a __pydantic_config__ attribute that we don't want to warn about
        has_dataclass_base = any(dataclasses.is_dataclass(base) for base in cls.__bases__)
        if not has_dataclass_base and config is not None and hasattr(cls, '__pydantic_config__'):
            warn(
                f'`config` is set via both the `dataclass` decorator and `__pydantic_config__` for dataclass {cls.__name__}. '
                f'The `config` specification from `dataclass` decorator will take priority.',
                category=UserWarning,
                stacklevel=2,
            )

        # if config is not explicitly provided, try to read it from the type
        config_dict = config if config is not None else getattr(cls, '__pydantic_config__', None)
        config_wrapper = _config.ConfigWrapper(config_dict)
        decorators = _decorators.DecoratorInfos.build(cls, replace_wrapped_methods=True)
        decorators.update_from_config(config_wrapper)

        # Keep track of the original __doc__ so that we can restore it after applying the dataclasses decorator
        # Otherwise, classes with no __doc__ will have their signature added into the JSON schema description,
        # since dataclasses.dataclass will set this as the __doc__
        original_doc = cls.__doc__

        if _pydantic_dataclasses.is_stdlib_dataclass(cls):
            # Vanilla dataclasses include a default docstring (representing the class signature),
            # which we don't want to preserve.
            original_doc = None

            # We don't want to add validation to the existing std lib dataclass, so we will subclass it
            #   If the class is generic, we need to make sure the subclass also inherits from Generic
            #   with all the same parameters.
            bases = (cls,)
            if issubclass(cls, Generic):
                generic_base = Generic[cls.__parameters__]  # type: ignore
                bases = bases + (generic_base,)
            cls = types.new_class(cls.__name__, bases)

        # Respect frozen setting from dataclass constructor and fallback to config setting if not provided
        if frozen is not None:
            frozen_ = frozen
            if config_wrapper.frozen:
                # It's not recommended to define both, as the setting from the dataclass decorator will take priority.
                warn(
                    f'`frozen` is set via both the `dataclass` decorator and `config` for dataclass {cls.__name__!r}.'
                    'This is not recommended. The `frozen` specification on `dataclass` will take priority.',
                    category=UserWarning,
                    stacklevel=2,
                )
        else:
            frozen_ = config_wrapper.frozen or False

        # Make Pydantic's `Field()` function compatible with stdlib dataclasses. As we'll decorate
        # `cls` with the stdlib `@dataclass` decorator first, there are two attributes, `kw_only` and
        # `repr` that need to be understood *during* the stdlib creation. We do so in two steps:

        # 1. On the decorated class, wrap `Field()` assignment with `dataclass.field()`, with the
        # two attributes set (done in `as_dataclass_field()`)
        cls_anns = _typing_extra.safe_get_annotations(cls)
        for field_name in cls_anns:
            # We should look for assignments in `__dict__` instead, but for now we follow
            # the same behavior as stdlib dataclasses (see https://github.com/python/cpython/issues/88609)
            field_value = getattr(cls, field_name, None)
            if isinstance(field_value, FieldInfo):
                setattr(cls, field_name, _pydantic_dataclasses.as_dataclass_field(field_value))

        # 2. For bases of `cls` that are stdlib dataclasses, we temporarily patch their fields
        # (see the docstring of the context manager):
        with _pydantic_dataclasses.patch_base_fields(cls):
            cls = dataclasses.dataclass(  # pyright: ignore[reportCallIssue]
                cls,
                # the value of init here doesn't affect anything except that it makes it easier to generate a signature
                init=True,
                repr=repr,
                eq=eq,
                order=order,
                unsafe_hash=unsafe_hash,
                frozen=frozen_,
                **kwargs,
            )

        if config_wrapper.validate_assignment:
            original_setattr = cls.__setattr__

            @functools.wraps(cls.__setattr__)
            def validated_setattr(instance: PydanticDataclass, name: str, value: Any, /) -> None:
                if frozen_:
                    return original_setattr(instance, name, value)  # pyright: ignore[reportCallIssue]
                inst_cls = type(instance)
                attr = getattr(inst_cls, name, None)

                if isinstance(attr, property):
                    attr.__set__(instance, value)
                elif isinstance(attr, functools.cached_property):
                    instance.__dict__.__setitem__(name, value)
                else:
                    inst_cls.__pydantic_validator__.validate_assignment(instance, name, value)

            cls.__setattr__ = validated_setattr.__get__(None, cls)  # type: ignore

            if slots and not hasattr(cls, '__setstate__'):
                # If slots is set, `pickle` (relied on by `copy.copy()`) will use
                # `__setattr__()` to reconstruct the dataclass. However, the custom
                # `__setattr__()` set above relies on `validate_assignment()`, which
                # in turn expects all the field values to be already present on the
                # instance, resulting in attribute errors.
                # As such, we make use of `object.__setattr__()` instead.
                # Note that we do so only if `__setstate__()` isn't already set (this is the
                # case if on top of `slots`, `frozen` is used).

                # Taken from `dataclasses._dataclass_get/setstate()`:
                def _dataclass_getstate(self: Any) -> list[Any]:
                    return [getattr(self, f.name) for f in dataclasses.fields(self)]

                def _dataclass_setstate(self: Any, state: list[Any]) -> None:
                    for field, value in zip(dataclasses.fields(self), state):
                        object.__setattr__(self, field.name, value)

                cls.__getstate__ = _dataclass_getstate  # pyright: ignore[reportAttributeAccessIssue]
                cls.__setstate__ = _dataclass_setstate  # pyright: ignore[reportAttributeAccessIssue]

        # This is an undocumented attribute to distinguish stdlib/Pydantic dataclasses.
        # It should be set as early as possible:
        cls.__is_pydantic_dataclass__ = True
        cls.__pydantic_decorators__ = decorators  # type: ignore
        cls.__doc__ = original_doc
        # Can be non-existent for dynamically created classes:
        firstlineno = getattr(original_cls, '__firstlineno__', None)
        cls.__module__ = original_cls.__module__
        if sys.version_info >= (3, 13) and firstlineno is not None:
            # As per https://docs.python.org/3/reference/datamodel.html#type.__firstlineno__:
            # Setting the `__module__` attribute removes the `__firstlineno__` item from the type’s dictionary.
            original_cls.__firstlineno__ = firstlineno
            cls.__firstlineno__ = firstlineno
        cls.__qualname__ = original_cls.__qualname__
        cls.__pydantic_fields_complete__ = classmethod(_pydantic_fields_complete)
        cls.__pydantic_complete__ = False  # `complete_dataclass` will set it to `True` if successful.
        # TODO `parent_namespace` is currently None, but we could do the same thing as Pydantic models:
        # fetch the parent ns using `parent_frame_namespace` (if the dataclass was defined in a function),
        # and possibly cache it (see the `__pydantic_parent_namespace__` logic for models).
        _pydantic_dataclasses.complete_dataclass(cls, config_wrapper, raise_errors=False)
        return cls

    return create_dataclass if _cls is None else create_dataclass(_cls)


def dataclass(
    _cls: Optional[Type[_T]] = None,
    *,
    init: bool = True,
    repr: bool = True,
    eq: bool = True,
    order: bool = False,
    unsafe_hash: bool = False,
    frozen: bool = False,
    config: Union[ConfigDict, Type[object], None] = None,
    validate_on_init: Optional[bool] = None,
    use_proxy: Optional[bool] = None,
    kw_only: bool = False,
) -> Union[Callable[[Type[_T]], 'DataclassClassOrWrapper'], 'DataclassClassOrWrapper']:
    """
    Like the python standard lib dataclasses but with type validation.
    The result is either a pydantic dataclass that will validate input data
    or a wrapper that will trigger validation around a stdlib dataclass
    to avoid modifying it directly
    """
    the_config = get_config(config)

    def wrap(cls: Type[Any]) -> 'DataclassClassOrWrapper':
        should_use_proxy = (
            use_proxy
            if use_proxy is not None
            else (
                is_builtin_dataclass(cls)
                and (cls.__bases__[0] is object or set(dir(cls)) == set(dir(cls.__bases__[0])))
            )
        )
        if should_use_proxy:
            dc_cls_doc = ''
            dc_cls = DataclassProxy(cls)
            default_validate_on_init = False
        else:
            dc_cls_doc = cls.__doc__ or ''  # needs to be done before generating dataclass
            if sys.version_info >= (3, 10):
                dc_cls = dataclasses.dataclass(
                    cls,
                    init=init,
                    repr=repr,
                    eq=eq,
                    order=order,
                    unsafe_hash=unsafe_hash,
                    frozen=frozen,
                    kw_only=kw_only,
                )
            else:
                dc_cls = dataclasses.dataclass(  # type: ignore
                    cls, init=init, repr=repr, eq=eq, order=order, unsafe_hash=unsafe_hash, frozen=frozen
                )
            default_validate_on_init = True

        should_validate_on_init = default_validate_on_init if validate_on_init is None else validate_on_init
        _add_pydantic_validation_attributes(cls, the_config, should_validate_on_init, dc_cls_doc)
        dc_cls.__pydantic_model__.__try_update_forward_refs__(**{cls.__name__: cls})
        return dc_cls

    if _cls is None:
        return wrap

    return wrap(_cls)


def dataclass(cls=None, extra_fields=None, **kwargs):
  """Wrapper for dataclasses.dataclass that adds support for kw_only fields.

  Args:
    cls: The class to transform (or none to return a decorator).
    extra_fields: A list of `(name, type, Field)` tuples describing extra fields
      that should be added to the dataclass.  This is necessary for linen's
      use-case of this module, since the base class (linen.Module) is *not* a
      dataclass.  In particular, linen.Module class is used as the base for both
      frozen and non-frozen dataclass subclasses; but the frozen status of a
      dataclass must match the frozen status of any base dataclasses.
    **kwargs: Additional arguments for `dataclasses.dataclass`.

  Returns:
    `cls`.
  """

  def wrap(cls):
    return _process_class(cls, extra_fields=extra_fields, **kwargs)

  return wrap if cls is None else wrap(cls)


def dataclass(cls: type[A], /) -> type[A]: ...


def dataclass(
  *,
  init: bool = True,
  eq: bool = True,
  order: bool = False,
  unsafe_hash: bool = False,
  match_args: bool = True,
  kw_only: bool = False,
  slots: bool = False,
  weakref_slot: bool = False,
) -> tp.Callable[[type[A]], type[A]]: ...


def dataclass(
  cls=None,
  /,
  *,
  init: bool = True,
  eq: bool = True,
  order: bool = False,
  unsafe_hash: bool = False,
  match_args: bool = True,
  kw_only: bool = False,
  slots: bool = False,
  weakref_slot: bool = False,
) -> tp.Any:
  return dataclasses.dataclass(
    cls,
    init=init,
    eq=eq,
    order=order,
    unsafe_hash=unsafe_hash,
    match_args=match_args,
    kw_only=kw_only,
    slots=slots,
    weakref_slot=weakref_slot,
  )


def dataclass(
    cls: None = ...,
    *,
    kw_only: bool = ...,
    replace: bool = ...,  # pylint: disable=redefined-outer-name
    repr: bool = ...,  # pylint: disable=redefined-builtin
    auto_cast: bool = ...,
    contextvars: bool = ...,
    allow_unfrozen: bool = ...,
) -> Callable[[_ClsT], _ClsT]:
  ...


def dataclass(
    cls: _ClsT,
    *,
    kw_only: bool = ...,
    replace: bool = ...,  # pylint: disable=redefined-outer-name
    repr: bool = ...,  # pylint: disable=redefined-builtin
    auto_cast: bool = ...,
    contextvars: bool = ...,
    allow_unfrozen: bool = ...,
) -> _ClsT:
  ...


def dataclass(
    cls=None,
    *,
    kw_only=False,
    replace=True,  # pylint: disable=redefined-outer-name
    repr=True,  # pylint: disable=redefined-builtin
    auto_cast=True,
    contextvars=True,
    allow_unfrozen=False,
):
  """Augment a dataclass with additional features.

  `auto_cast`: Auto-convert init assignements to the annotated class.

  ```python
  @edc.dataclass
  class A:
    path: edc.AutoCast[epath.Path]
    some_enum: edc.AutoCast[MyEnum]
    x: edc.AutoCast[str]

  a = A(
      path='/some/path',
      some_enum='A',
      x=123
  )
  # Fields annotated with `AutoCast` are automatically casted to their type
  assert a.path == epath.Path('/some/path')
  assert a.some_enum is MyEnum.A
  assert a.x == '123'
  ```

  `allow_unfrozen`: allow nested dataclass to be updated. This add two methods:

   * `.unfrozen()`: Create a lazy deep-copy of the current dataclass. Updates
     to nested attributes will be propagated to the top-level dataclass.
   * `.frozen()`: Returns the frozen dataclass, after it was mutated.

  Example:

  ```python
  old_x = X(y=Y(z=123))

  x = old_x.unfrozen()
  x.y.z = 456
  x = x.frozen()

  assert x == X(y=Y(z=123))  # Only new x is mutated
  assert old_x == X(y=Y(z=456))  # Old x is not mutated
  ```

  Note:

  * Only the last `.frozen()` call resolve the dataclass by calling `.replace`
    recursivelly.
  * Dataclass returned by `.unfrozen()` and nested attributes are not the
    original dataclass but proxy objects which track the mutations. As such,
    those object are not compatible with `isinstance()`, `jax.tree.map`,...
  * Only the top-level dataclass need to be `allow_unfrozen=True`
  * Avoid using `unfrozen` if 2 attributes of the dataclass point to the
    same nested dataclass. Updates on one attribute might not be reflected on
    the other.

    ```python
    y = Y(y=123)
    x = X(x0=y, x1=y)  # Same instance assigned twice in `x0` and `x1`
    x = x.unfrozen()
    x.x0.y = 456  # Changes in `x0` not reflected in `x1`
    x = x.frozen()

    assert x == X(x0=Y(y=456), x1=Y(y=123))
    ```

    This is because only attributes which are accessed are tracked, so `etils`
    do not know the object exist somewhere else in the attribute tree.

  * After `.frozen()` has been called, any of the temporary sub-attribute
    become invalid:

    ```python
    a = a.unfrozen()
    y = a.y
    a = a.frozen()

    y.x  # Raise error (created between the unfrozen/frozen call)
    a.y.x  # Work
    ```

  `contextvars`: Fields annotated as `edc.ContextVar` are wrapped in
  a `contextvars.ContextVar`. Afterward each thread / asyncio coroutine will
  have its own version of the fields (similarly to `threading.local`).

  The contextvars are lazily initialized at first usage.

  Example:

  ```python
  @edc.dataclass
  @dataclasses.dataclass
  class Context:
    thread_id: edc.ContextVar[int] = dataclasses.field(
        default_factory=threading.get_native_id
    )
    stack: edc.ContextVar[list[str]] = dataclasses.field(default_factory=list)

  # Global context object
  context = Context(thread_id=0)

  def worker():
    # Inside each thread, the worker use its own context
    assert context.thread_id != 0
    context.stack.append(1)

  with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    for _ in range(10):
      executor.submit(worker)
  ```

  Args:
    cls: The dataclass to decorate
    kw_only: If True, make the dataclass `__init__` keyword-only.
    replace: If `True`, add a `.replace(` alias of `dataclasses.replace`.
    repr: If `True`, the class `__repr__` will return a pretty-printed `str`
      (one attribute per line)
    auto_cast: If `True`, fields annotated as `x: edc.AutoCast[Cls]` will be
      converted to `x: Cls = edc.field(validator=Cls)`.
    contextvars: It `True`, fields annotated as `x: edc.AutoCast[T]` are
      converted to `contextvars`. This allow to have a `threading.local`-like
      API for contextvars.
    allow_unfrozen: If `True`, add `.frozen`, `.unfrozen` methods.

  Returns:
    Decorated class
  """
  # Return decorator
  if cls is None:
    return functools.partial(
        dataclass,
        kw_only=kw_only,
        replace=replace,
        repr=repr,
        auto_cast=auto_cast,
        allow_unfrozen=allow_unfrozen,
    )

  if kw_only:
    cls = _make_kw_only(cls)

  if repr:
    cls = add_repr(cls)

  if replace:
    cls = _add_replace(cls)

  if allow_unfrozen:
    cls = frozen_utils.add_unfrozen(cls)

  descriptor_fns = []
  if auto_cast:
    descriptor_fns.append(
        helpers.DescriptorInfo(
            annotation=cast_utils.AutoCast,
            descriptor_fn=cast_utils.make_auto_cast_descriptor,
        )
    )

  if contextvars:
    descriptor_fns.append(
        helpers.DescriptorInfo(
            annotation=context.ContextVar,
            descriptor_fn=context.make_contextvar_descriptor,
        )
    )

  cls = helpers.wrap_new(cls, descriptor_fns)

  return cls


def dataclass(
    cls=None,
    *,
    init=True,
    repr=True,  # pylint: disable=redefined-builtin
    eq=True,
    order=False,
    unsafe_hash=False,
    frozen=False,
    kw_only: bool = False,
    mappable_dataclass=True,  # pylint: disable=redefined-outer-name
):
  """JAX-friendly wrapper for :py:func:`dataclasses.dataclass`.

  This wrapper class registers new dataclasses with JAX so that tree utils
  operate correctly. Additionally a replace method is provided making it easy
  to operate on the class when made immutable (frozen=True).

  Args:
    cls: A class to decorate.
    init: See :py:func:`dataclasses.dataclass`.
    repr: See :py:func:`dataclasses.dataclass`.
    eq: See :py:func:`dataclasses.dataclass`.
    order: See :py:func:`dataclasses.dataclass`.
    unsafe_hash: See :py:func:`dataclasses.dataclass`.
    frozen: See :py:func:`dataclasses.dataclass`.
    kw_only: See :py:func:`dataclasses.dataclass`.
    mappable_dataclass: If True (the default), methods to make the class
      implement the :py:class:`collections.abc.Mapping` interface will be
      generated and the class will include :py:class:`collections.abc.Mapping`
      in its base classes.
      `True` is the default, because being an instance of `Mapping` makes
      `chex.dataclass` compatible with e.g. `jax.tree_util.tree_*` methods, the
      `tree` library, or methods related to tensorflow/python/utils/nest.py.
      As a side-effect, e.g. `np.testing.assert_array_equal` will only check
      the field names are equal and not the content. Use `chex.assert_tree_*`
      instead.

  Returns:
    A JAX-friendly dataclass.
  """
  def dcls(cls):
    # Make sure to create a separate _Dataclass instance for each `cls`.
    return _Dataclass(
        init, repr, eq, order, unsafe_hash, frozen, kw_only, mappable_dataclass
    )(cls)

  if cls is None:
    return dcls
  return dcls(cls)

