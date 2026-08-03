import re
import sys

def update_global_namespace(
    *,
    reload: list[str],
    verbose: bool,
) -> None:
  """Overwrite the imported modules in the current Colab global namespace."""
  reload = set(reload)

  ip = IPython.get_ipython()
  user_ns = ip.kernel.shell.user_ns

  # Filter only the modules
  # This means that `from module import function` or `from module import *`
  # won't be reloaded
  # Note that we overwrite all modules which match, not only the ones defined
  # inside the `adhoc` contextmanager. It's not trivial to detect when a module
  # is re-imported, like:
  #
  # import module
  # with ecolab.adhoc():
  #   import module  # < globals() not modified, difficult to detect
  #
  for name, module in dict(user_ns).items():
    # We look at all globals, not just the ones defined inside the
    # contextmanager.
    # The solution would be to mock `__import__` to capture all statements
    # but over-engineered for now.
    if not isinstance(module, types.ModuleType):
      continue  # The object is not a module

    # `getattr_static` for `lazy_imports` modules
    module_name = inspect.getattr_static(module, '__name__', None)
    if module_name not in reload:
      continue  # The module not reloaded
    if re.fullmatch(r'_+(\d+)?', name):
      continue  # Internal IPython variables (`_`, `__`, `_12`)

    if verbose:
      print(f'Overwrting Colab global {name!r} to new module ({module_name!r})')

    reloaded_module = sys.modules[module_name]
    user_ns[name] = reloaded_module

