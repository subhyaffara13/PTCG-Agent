from typing import Callable

def register_path_cls(
    path_cls_or_uri_prefix: str | list[str] | tuple[str, ...]
) -> Callable[[_T], _T]:
  ...


def register_path_cls(path_cls_or_uri_prefix: _T) -> _T:
  ...


def register_path_cls(path_cls_or_uri_prefix):
  """Register the pathlib-like class.

  ```python
  @epath.register_path_cls('my_path://')
  class MyPath(pathlib.PurePosixPath):
    ...

  my_path = epath.Path('my_path://some-path')
  assert isinstance(my_path, MyPath)
  ```

  Args:
    path_cls_or_uri_prefix: If a uri prefix is given, then passing calling
      `tfds.core.as_path('prefix://path')` will call the decorated class.

  Returns:
    The decorator or decoratorated class
  """
  global _PATHLIKE_CLS
  if isinstance(path_cls_or_uri_prefix, (str, list, tuple)):

    def register_path_cls_decorator(cls: _T) -> _T:
      if isinstance(path_cls_or_uri_prefix, str):
        _URI_PREFIXES_TO_CLS[path_cls_or_uri_prefix] = cls
      elif isinstance(path_cls_or_uri_prefix, (list, tuple)):
        for uri_prefix in path_cls_or_uri_prefix:
          _URI_PREFIXES_TO_CLS[uri_prefix] = cls
      return register_path_cls(cls)

    return register_path_cls_decorator
  else:
    _PATHLIKE_CLS = _PATHLIKE_CLS + (path_cls_or_uri_prefix,)
    return path_cls_or_uri_prefix

