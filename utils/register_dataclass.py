
def register_dataclass(
    cls: type[Any],
    *,
    serialized_type_name: str | None = None,
) -> None:
    """
    Registers a dataclass as a valid input/output type for :func:`torch.export.export`.

    Args:
        cls: the dataclass type to register
        serialized_type_name: The serialized name for the dataclass. This is
        required if you want to serialize the pytree TreeSpec containing this
        dataclass.

    Example::

        import torch
        from dataclasses import dataclass


        @dataclass
        class InputDataClass:
            feature: torch.Tensor
            bias: int


        @dataclass
        class OutputDataClass:
            res: torch.Tensor


        torch.export.register_dataclass(InputDataClass)
        torch.export.register_dataclass(OutputDataClass)


        class Mod(torch.nn.Module):
            def forward(self, x: InputDataClass) -> OutputDataClass:
                res = x.feature + x.bias
                return OutputDataClass(res=res)


        ep = torch.export.export(Mod(), (InputDataClass(torch.ones(2, 2), 1),))
        print(ep)

    """
    pytree.register_dataclass(cls, serialized_type_name=serialized_type_name)


def register_dataclass(
    cls: type[Any],
    *,
    field_names: list[str] | None = None,
    drop_field_names: list[str] | None = None,
    serialized_type_name: str | None = None,
) -> None:
    """
    Registers a type that has the semantics of a ``dataclasses.dataclass`` type
    as a pytree node.

    This is a simpler API than :func:`register_pytree_node` for registering
    a dataclass or a custom class with the semantics of a dataclass.

    Args:
        cls: The python type to register. The class must have the semantics of a
        dataclass; in particular, it must be constructed by passing the fields
        in.
        field_names (Optional[List[str]]): A list of field names that correspond
            to the **non-constant data** in this class. This list must contain
            all the fields that are used to initialize the class. This argument
            is optional if ``cls`` is a dataclass, in which case the fields will
            be taken from ``dataclasses.fields()``.
        drop_field_names (Optional[List[str]]): A list of field names that
            should not be included in the pytree.
        serialized_type_name: A keyword argument used to specify the fully
            qualified name used when serializing the tree spec. This is only
            needed for serializing the treespec in torch.export.

    Example:

        >>> from torch import Tensor
        >>> from dataclasses import dataclass
        >>> import torch.utils._pytree as pytree
        >>>
        >>> @dataclass
        >>> class Point:
        >>>     x: Tensor
        >>>     y: Tensor
        >>>
        >>> pytree.register_dataclass(Point)
        >>>
        >>> point = Point(torch.tensor(0), torch.tensor(1))
        >>> point = pytree.tree_map(lambda x: x + 1, point)
        >>> assert torch.allclose(point.x, torch.tensor(1))
        >>> assert torch.allclose(point.y, torch.tensor(2))

    """
    drop_field_names = drop_field_names or []

    if not dataclasses.is_dataclass(cls):
        if field_names is None:
            raise ValueError(
                "field_names must be specified with a list of all fields used to "
                f"initialize {cls}, as it is not a dataclass."
            )
    elif field_names is None:
        field_names = [f.name for f in dataclasses.fields(cls) if f.init]
    else:
        dataclass_init_fields = {f.name for f in dataclasses.fields(cls) if f.init}
        dataclass_init_fields.difference_update(drop_field_names)

        if dataclass_init_fields != set(field_names):
            error_msg = "field_names does not include all dataclass fields.\n"

            if missing := dataclass_init_fields - set(field_names):
                error_msg += (
                    f"Missing fields in `field_names`: {missing}. If you want "
                    "to include these fields in the pytree, please add them "
                    "to `field_names`, otherwise please add them to "
                    "`drop_field_names`.\n"
                )

            if unexpected := set(field_names) - dataclass_init_fields:
                error_msg += (
                    f"Unexpected fields in `field_names`: {unexpected}. "
                    "Please remove these fields, or add them to `drop_field_names`.\n"
                )

            raise ValueError(error_msg)

    def _flatten_fn(obj: Any) -> tuple[list[Any], Context]:
        flattened = []
        flat_names = []
        none_names = []
        for name in field_names:
            val = getattr(obj, name)
            if val is not None:
                flattened.append(val)
                flat_names.append(name)
            else:
                none_names.append(name)
        return flattened, [flat_names, none_names]

    def _unflatten_fn(values: Iterable[Any], context: Context) -> Any:
        flat_names, none_names = context
        return cls(
            **dict(zip(flat_names, values, strict=True)), **dict.fromkeys(none_names)
        )

    def _flatten_fn_with_keys(obj: Any) -> tuple[list[Any], Context]:
        flattened, (flat_names, _none_names) = _flatten_fn(obj)  # type: ignore[misc]
        return [
            (GetAttrKey(k), v) for k, v in zip(flat_names, flattened, strict=True)
        ], flat_names

    _private_register_pytree_node(
        cls,
        _flatten_fn,
        _unflatten_fn,
        serialized_type_name=serialized_type_name,
        flatten_with_keys_fn=_flatten_fn_with_keys,
    )


def register_dataclass(
    nodetype: Typ,
    data_fields: Sequence[str] | None = None,
    meta_fields: Sequence[str] | None = None,
    drop_fields: Sequence[str] = (),
) -> Typ:
  """Extends the set of types that are considered internal nodes in pytrees.

  This differs from ``register_pytree_with_keys_class`` in that the C++
  registries use the optimized C++ dataclass builtin instead of the argument
  functions.

  See :ref:`pytrees-custom-pytree-nodes` for more information about registering pytrees.

  Args:
    nodetype: a Python type to treat as an internal pytree node. This is assumed
      to have the semantics of a :obj:`~dataclasses.dataclass`: namely, class
      attributes represent the whole of the object state, and can be passed
      as keywords to the class constructor to create a copy of the object.
      All defined attributes should be listed among ``meta_fields`` or ``data_fields``.
    meta_fields: metadata field names: these are attributes which will be treated as
      :term:`static` when this pytree is passed to :func:`jax.jit`. ``meta_fields`` is
      optional only if ``nodetype`` is a dataclass, in which case individual fields can
      be marked static via :func:`dataclasses.field` (see examples below).
      Metadata fields *must* be static, hashable, immutable objects, as these objects
      are used to generate JIT cache keys. In particular, metadata fields cannot contain
      :class:`jax.Array` or :class:`numpy.ndarray` objects.
    data_fields: data field names: these are attributes which will be treated as non-static
      when this pytree is passed to :func:`jax.jit`. ``data_fields`` is optional only if
      ``nodetype`` is a dataclass, in which case fields are assumed data fields unless
      marked via :func:`dataclasses.field` (see examples below).
      Data fields *must* be JAX-compatible objects such as arrays (:class:`jax.Array`
      or :class:`numpy.ndarray`), scalars, or pytrees whose leaves are arrays or scalars.
      Note that ``None`` is a valid data field, as JAX recognizes this as an empty pytree.
    drop_fields: only referenced if ``nodetype`` is a dataclass. Specify a sequence of
      field names from among ``dataclasses.fields(nodetype)`` to be excluded from pytree
      registration.

  Returns:
    The input class ``nodetype`` is returned unchanged after being added to JAX's
    pytree registry, so that :func:`register_dataclass` can be used as a decorator.

  Examples:
    In JAX v0.4.35 or older, you must specify ``data_fields`` and ``meta_fields``
    in order to use this decorator:

    >>> import jax
    >>> from dataclasses import dataclass
    >>> from functools import partial
    ...
    >>> @partial(jax.tree_util.register_dataclass,
    ...          data_fields=['x', 'y'],
    ...          meta_fields=['op'])
    ... @dataclass
    ... class MyStruct:
    ...   x: jax.Array
    ...   y: jax.Array
    ...   op: str
    ...
    >>> m = MyStruct(x=jnp.ones(3), y=jnp.arange(3), op='add')
    >>> m
    MyStruct(x=Array([1., 1., 1.], dtype=float32), y=Array([0, 1, 2], dtype=int32), op='add')

    Starting in JAX v0.4.36, the ``data_fields`` and ``meta_fields`` arguments are optional
    for :func:`~dataclasses.dataclass` inputs, with fields defaulting to ``data_fields``
    unless marked as static using `static` metadata in :func:`dataclasses.field`.

    >>> import jax
    >>> from dataclasses import dataclass, field
    ...
    >>> @jax.tree_util.register_dataclass
    ... @dataclass
    ... class MyStruct:
    ...   x: jax.Array  # defaults to non-static data field
    ...   y: jax.Array  # defaults to non-static data field
    ...   op: str = field(metadata=dict(static=True))  # marked as static meta field.
    ...
    >>> m = MyStruct(x=jnp.ones(3), y=jnp.arange(3), op='add')
    >>> m
    MyStruct(x=Array([1., 1., 1.], dtype=float32), y=Array([0, 1, 2], dtype=int32), op='add')

    Once this class is registered, it can be used with functions in :mod:`jax.tree` and
    :mod:`jax.tree_util`:

    >>> leaves, treedef = jax.tree.flatten(m)
    >>> leaves
    [Array([1., 1., 1.], dtype=float32), Array([0, 1, 2], dtype=int32)]
    >>> treedef
    PyTreeDef(CustomNode(MyStruct[('add',)], [*, *]))
    >>> jax.tree.unflatten(treedef, leaves)
    MyStruct(x=Array([1., 1., 1.], dtype=float32), y=Array([0, 1, 2], dtype=int32), op='add')

    In particular, this registration allows ``m`` to be passed seamlessly through code
    wrapped in :func:`jax.jit` and other JAX transformations, with ``data_fields`` being
    treated as dynamic arguments, and ``meta_fields`` being treated as static arguments:

    >>> @jax.jit
    ... def compiled_func(m):
    ...   if m.op == 'add':
    ...     return m.x + m.y
    ...   else:
    ...     raise ValueError(f"{m.op=}")
    ...
    >>> compiled_func(m)
    Array([1., 2., 3.], dtype=float32)
  """
  if data_fields is None or meta_fields is None:
    if (data_fields is None) != (meta_fields is None):
      raise TypeError("register_dataclass: data_fields and meta_fields must both be specified"
                      f" when either is specified. Got {data_fields=} {meta_fields=}.")
    if not dataclasses.is_dataclass(nodetype):
      raise TypeError("register_dataclass: data_fields and meta_fields are required when"
                      f" nodetype is not a dataclass. Got {nodetype=}.")
    data_fields = [
        f.name
        for f in dataclasses.fields(nodetype)
        if not f.metadata.get("static", False)
    ]
    meta_fields = [
        f.name
        for f in dataclasses.fields(nodetype)
        if f.metadata.get("static", False)
    ]

  assert meta_fields is not None
  assert data_fields is not None

  # Store inputs as immutable tuples in this scope, because we close over them
  # for later evaluation. This prevents potentially confusing behavior if the
  # caller were to pass in lists that are later mutated.
  meta_fields = tuple(meta_fields)
  data_fields = tuple(data_fields)

  if dataclasses.is_dataclass(nodetype):
    init_fields = {f.name for f in dataclasses.fields(nodetype) if f.init}
    init_fields.difference_update(drop_fields)
    if {*meta_fields, *data_fields} != init_fields:
      msg = (
          "data_fields and meta_fields must include all dataclass fields with"
          " ``init=True`` and only them."
      )
      if missing := init_fields - {*meta_fields, *data_fields}:
        msg += (
            f" Missing fields: {missing}. Add them to drop_fields to suppress"
            " this error."
        )
      if unexpected := {*meta_fields, *data_fields} - init_fields:
        msg += f" Unexpected fields: {unexpected}."
      raise ValueError(msg)

  if overlap := set(data_fields) & set(meta_fields):
    raise ValueError(
        "data_fields and meta_fields must not overlap. Overlapping fields:"
        f" {overlap}."
    )

  def unflatten_func(meta, data):
    meta_args = tuple(zip(meta_fields, meta))
    data_args = tuple(zip(data_fields, data))
    kwargs = dict(meta_args + data_args)
    return nodetype(**kwargs)

  def flatten_func(x):
    meta = tuple(getattr(x, name) for name in meta_fields)
    data = tuple(getattr(x, name) for name in data_fields)
    return data, meta

  for registry in _all_registries:
    registry.register_dataclass_node(nodetype, list(data_fields), list(meta_fields))
  _registry[nodetype] = _RegistryEntry(flatten_func, unflatten_func)
  return nodetype

