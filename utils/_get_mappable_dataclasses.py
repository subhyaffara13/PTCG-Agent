from typing import Any

def _get_mappable_dataclasses(test_type):
  """Generates shallow and nested mappable dataclasses."""

  class Class:
    """Shallow class."""

    k_tuple: tuple  # pylint:disable=g-bare-generic
    k_dict: dict  # pylint:disable=g-bare-generic

    def some_method(self, *args):
      raise RuntimeError('Class.some_method() was called.')

  class NestedClass:
    """Nested class."""

    k_any: Any
    k_int: int
    k_str: str
    k_arr: np.ndarray
    k_dclass_with_map: Class
    k_dclass_no_map: ClassWithoutMap
    k_dict_factory: dict = dataclasses.field(  # pylint:disable=g-bare-generic,invalid-field-call
        default_factory=lambda: dict(x='x', y='y'))
    k_default: str = 'default_str'
    k_non_init: int = dataclasses.field(default=1, init=False)  # pylint:disable=g-bare-generic,invalid-field-call
    k_init_only: dataclasses.InitVar[int] = 10

    def some_method(self, *args):
      raise RuntimeError('NestedClassWithMap.some_method() was called.')

    def __post_init__(self, k_init_only):
      self.k_non_init = self.k_int * k_init_only

  if test_type == 'chex':
    cls = chex_dataclass(Class, mappable_dataclass=True)
    nested_cls = chex_dataclass(NestedClass, mappable_dataclass=True)
  elif test_type == 'original':
    cls = mappable_dataclass(orig_dataclass(Class))
    nested_cls = mappable_dataclass(orig_dataclass(NestedClass))
  else:
    raise ValueError(f'Unknown test type: {test_type}')

  return cls, nested_cls

