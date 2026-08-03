import functools
from typing import Any

def lazy_api_imports(
    globals_: dict[str, Any],
    *,
    error_msg: str | None = None,
) -> Iterator[None]:
  """Lazy-import an API (`__init__.py`).

  Usage:

  ```python
  with epy.lazy_api_imports(globals()):
    from my_project import Obj1
    from my_project import OtherObj
    from my_project import my_function
  ```

  Contrary to `epy.lazy_imports()` which works on modules (and resolve the
  imports) during first access. This function is intended to be used on
  `__init__.py` files, such as all imported symbols are lazy and only resolved
  when the symbol is accessed.

  Args:
    globals_: The module `globals()`. Will be updated to add a `__getattr__`
    error_msg: A additional message to append to the `ImportError` if the import
      fails. Can use `{symbol_name}` dynamic placeholder.

  Yields:
    None
  """
  try:
    before = set(globals_)
    with lazy_imports_utils.lazy_imports():
      yield
  finally:
    after = set(globals_)

  all_imported_symbols = after - before
  imported_symbols = {
      k: v
      for k in all_imported_symbols
      if isinstance(v := globals_[k], lazy_imports_utils.LazyModule)
  }
  if len(all_imported_symbols) != len(imported_symbols):
    raise ValueError(
        'Unexpected imported symbols: '
        f'{set(all_imported_symbols) - set(imported_symbols)}.'
    )
  for name in imported_symbols:
    del globals_[name]  # Remove so `module.__getattr__` is triggered

  # Note this will only works if the `__getattr__` is defined before the
  # `lazy_api_imports`, which is quite unlikely.
  assert '__getattr__' not in globals_
  assert '__dir__' not in globals_
  globals_['__getattr__'] = functools.partial(
      _getattr,
      module_name=globals_['__name__'],
      imported_symbols=imported_symbols,
      error_msg=error_msg,
  )
  globals_['__dir__'] = functools.partial(
      _dir,
      globals_=globals_,
      imported_symbols=imported_symbols,
  )

