import pathlib
import sys
from typing import Union

def resource_path(package: Union[str, types.ModuleType]) -> abstract_path.Path:
  """Returns read-only root directory path of the module.

  Used to access module resource files.

  Usage:

  ```python
  path = epath.resource_path('tensorflow_datasets') / 'README.md'
  content = path.read_text()
  ```

  This is compatible with everything, including zipapp (`.par`).

  Resource files should be in the `data=` of the `py_library(` (when using
  bazel).

  To write to your project (e.g. automatically update your code), read-only
  resource paths can be converted to read-write paths with
  `epath.to_write_path(path)`.

  Args:
    package: Module or module name.

  Returns:
    The read-only path to the root module directory
  """
  try:
    path = importlib_resources.files(package)  # pytype: disable=module-attr
  except AttributeError:
    is_adhoc = True
  else:
    is_adhoc = False

  if is_adhoc:
    # TODO(b/260333695): `importlib_resources` fail with adhoc imports
    # When module are imported with adhoc, `importlib_resources.files` returns
    # a non-path object, so convert manually.
    # Note this is not the true path (`/google_src/` vs
    # `/export/.../server/ml_notebook.runfiles`), but should be equivalent.
    # TODO(b/390190120): Note that `module.__name__` behave inconsistently.
    if isinstance(package, types.ModuleType):
      path = package.__file__
    elif isinstance(package, str):
      path = sys.modules[package].__file__
    else:
      raise TypeError(f'Unknown package type: {type(package)}: {package}')
    path = pathlib.Path(path)
    if path.name == '__init__.py':
      path = path.parent

  # pylint: disable=undefined-variable
  if isinstance(path, pathlib.Path):
    # TODO(etils): To ensure compatibility with zipfile.Path, we should ensure
    # that the returned `pathlib.Path` isn't missused. More specifically:
    # * `os.fspath` should only be called on files (not directories)
    # * `str(path)` should be forbidden (only `__format__` allowed).
    # In practice, it is trickier to do as `__fspath__` and `__str__` are
    # called internally.
    # Convert to `GPath` for consistency and compatibility with `MockFs`.
    return abstract_path.Path(path)
  elif isinstance(path, zipfile.Path):
    path = ResourcePath(path.root, path.at)
    return typing.cast(abstract_path.Path, path)
  elif isinstance(path, importlib_resources.abc.Traversable):
    # Is seems like `importlib_resources.files` can return additional types,
    # like `MultiplexedPath`.
    # Fallback to avoid failure, however those objects might not implement
    # `__fspath__`, so might fail later.
    return typing.cast(abstract_path.Path, path)
  else:
    raise TypeError(f'Unknown resource path: {type(path)}: {path}')

