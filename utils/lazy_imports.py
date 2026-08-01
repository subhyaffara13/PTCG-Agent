
def lazy_imports(
    *,
    error_callback: str | _ErrorCallback | None = None,
    success_callback: _SuccessCallback | None = None,
) -> Iterator[None]:
  """Context Manager which lazy loads packages.

  Their import is not executed immediately, but is postponed to the first
  call of one of their attributes.

  Limitation:

  - You can only lazy load modules (`from x import y` will not work if `y` is a
    constant or a function or a class).

  Usage:

  ```python
  with epy.lazy_imports():
    import tensorflow as tf

  with epy.lazy_imports(success_callback=check_tf_version):
    import tensorflow as tf
  ```

  When using type annotations, make sure to also use
  `from __future__ import annotations`, otherwise the lazy-import will be
  triggered at import time when used in typing annotations:

  ```pthon
  with epy.lazy_imports():
    import tensorflow as tf

  # !!! Resolve the lazy-import when `__future__.annotations` isn't present
  def get_dataset() -> tf.data.Dataset:
  ```

  This support `ecolab.adhoc` imports: When the lazy-import is resolved,
  the original `ecolab.adhoc` context is re-created to import the lazy module.

  Args:
    error_callback: A additional message to append to the `ImportError` if the
      import fails. Can also be a `Callable[[Exception], None]`. The exception
      is passed as an arg, so user can use `epy.reraise(e, 'Additional
      message')`.
    success_callback: a callback to trigger when an import succeeds. The
      callback is passed the name of the imported module as an arg.

  Yields:
    None
  """
  # Need to mock `__import__` (instead of `sys.meta_path`, as we do not want
  # to modify the `sys.modules` cache in any way)
  original_import = builtins.__import__
  try:
    builtins.__import__ = functools.partial(
        _lazy_import,
        error_callback=error_callback,
        success_callback=success_callback,
    )
    yield
  finally:
    builtins.__import__ = original_import

