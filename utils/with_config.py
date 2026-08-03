from typing import Any, Callable

def with_config(*, config: ConfigDict) -> Callable[[_TypeT], _TypeT]: ...


def with_config(config: ConfigDict, /) -> Callable[[_TypeT], _TypeT]: ...


def with_config(**config: Unpack[ConfigDict]) -> Callable[[_TypeT], _TypeT]: ...


def with_config(config: ConfigDict | None = None, /, **kwargs: Any) -> Callable[[_TypeT], _TypeT]:
    """!!! abstract "Usage Documentation"
        [Configuration with other types](../concepts/config.md#configuration-on-other-supported-types)

    A convenience decorator to set a [Pydantic configuration](config.md) on a `TypedDict` or a `dataclass` from the standard library.

    Although the configuration can be set using the `__pydantic_config__` attribute, it does not play well with type checkers,
    especially with `TypedDict`.

    !!! example "Usage"

        ```python
        from typing_extensions import TypedDict

        from pydantic import ConfigDict, TypeAdapter, with_config

        @with_config(ConfigDict(str_to_lower=True))
        class TD(TypedDict):
            x: str

        ta = TypeAdapter(TD)

        print(ta.validate_python({'x': 'ABC'}))
        #> {'x': 'abc'}
        ```

    /// deprecated-removed | v2.11 v3
    Passing `config` as a keyword argument.
    ///

    /// version-changed | v2.11
    Keyword arguments can be provided directly instead of a config dictionary.
    ///
    """
    if config is not None and kwargs:
        raise ValueError('Cannot specify both `config` and keyword arguments')

    if len(kwargs) == 1 and (kwargs_conf := kwargs.get('config')) is not None:
        warnings.warn(
            'Passing `config` as a keyword argument is deprecated. Pass `config` as a positional argument instead',
            category=PydanticDeprecatedSince211,
            stacklevel=2,
        )
        final_config = cast(ConfigDict, kwargs_conf)
    else:
        final_config = config if config is not None else cast(ConfigDict, kwargs)

    def inner(class_: _TypeT, /) -> _TypeT:
        # Ideally, we would check for `class_` to either be a `TypedDict` or a stdlib dataclass.
        # However, the `@with_config` decorator can be applied *after* `@dataclass`. To avoid
        # common mistakes, we at least check for `class_` to not be a Pydantic model.
        from ._internal._utils import is_model_class

        if is_model_class(class_):
            raise PydanticUserError(
                f'Cannot use `with_config` on {class_.__name__} as it is a Pydantic model',
                code='with-config-on-model',
            )
        class_.__pydantic_config__ = final_config
        return class_

    return inner


def with_config(**kwds):
  """Test case decorator for subclasses of JaxTestCase"""
  def decorator(cls):
    assert inspect.isclass(cls) and issubclass(cls, JaxTestCase), "@with_config can only wrap JaxTestCase class definitions."
    cls._default_thread_local_config = {}
    for b in cls.__bases__:
      if hasattr(b, "_default_thread_local_config"):
        cls._default_thread_local_config.update(b._default_thread_local_config)
    cls._default_thread_local_config.update(kwds)
    return cls
  return decorator

