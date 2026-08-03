from typing import Any

def static(prefix: str, path: PathLike, **kwargs: Any) -> StaticDef:
    return StaticDef(prefix, path, kwargs)


def static(value: A, /) -> A: ...


def static(
  *,
  default: A = dataclasses.MISSING,  # type: ignore[assignment]
  default_factory: tp.Callable[[], A] | None = None,
  init: bool = True,
  repr: bool = True,
  hash: bool | None = None,
  compare: bool = True,
  metadata: tp.Mapping[str, tp.Any] | None = None,
  kw_only: bool = False,
) -> tp.Any: ...


def static(value: tp.Any = MISSING, /, **kwargs) -> tp.Any:
  """Annotates a an attribute as static.

  The return value from `static` must be directly assigned to an Object
  attribute
  which will be registered as static attribute.

  Example::

    from flax import nnx

    class Foo(nnx.Pytree):
      def __init__(self, a, b):
        self.a = nnx.static(a)  # pytree metadata
        self.b = nnx.data(b)    # pytree data

    foo = Foo("one", "two")

    assert jax.tree.leaves(foo) == ["two"]

  By default ``nnx.Pytree`` will ...
  """
  if not isinstance(value, Missing) and kwargs:
    raise TypeError(
      'nnx.static() accepts either a single positional argument or keyword'
      ' arguments, but not both.'
    )
  metadata = {'nnx_value': value}
  if 'metadata' in kwargs and kwargs['metadata'] is not None:
    if 'static' in kwargs['metadata']:
      raise ValueError(
        "Cannot use 'static' key in metadata argument for nnx.static."
      )
    metadata.update(kwargs.pop('metadata'))
  metadata['static'] = True
  return dataclasses.field(**kwargs, metadata=metadata)  # type: ignore[return-value]

