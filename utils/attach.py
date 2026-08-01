
def attach(module_name, submodules=None, submod_attrs=None):
    """Attach lazily loaded submodules, and functions or other attributes.

    Typically, modules import submodules and attributes as follows::

      import mysubmodule
      import anothersubmodule

      from .foo import someattr

    The idea of  this function is to replace the `__init__.py`
    module's `__getattr__`, `__dir__`, and `__all__` attributes such that
    all imports work exactly the way they normally would, except that the
    actual import is delayed until the resulting module object is first used.

    The typical way to call this function, replacing the above imports, is::

      __getattr__, __lazy_dir__, __all__ = lazy.attach(
          __name__, ["mysubmodule", "anothersubmodule"], {"foo": "someattr"}
      )

    This functionality requires Python 3.7 or higher.

    Parameters
    ----------
    module_name : str
        Typically use __name__.
    submodules : set
        List of submodules to lazily import.
    submod_attrs : dict
        Dictionary of submodule -> list of attributes / functions.
        These attributes are imported as they are used.

    Returns
    -------
    __getattr__, __dir__, __all__

    """
    if submod_attrs is None:
        submod_attrs = {}

    if submodules is None:
        submodules = set()
    else:
        submodules = set(submodules)

    attr_to_modules = {
        attr: mod for mod, attrs in submod_attrs.items() for attr in attrs
    }

    __all__ = list(submodules | attr_to_modules.keys())

    def __getattr__(name):
        if name in submodules:
            return importlib.import_module(f"{module_name}.{name}")
        elif name in attr_to_modules:
            submod = importlib.import_module(f"{module_name}.{attr_to_modules[name]}")
            return getattr(submod, name)
        else:
            raise AttributeError(f"No {module_name} attribute {name}")

    def __dir__():
        return __all__

    if os.environ.get("EAGER_IMPORT", ""):
        for attr in set(attr_to_modules.keys()) | submodules:
            __getattr__(attr)

    return __getattr__, __dir__, list(__all__)


def attach(package_name: str, submodules: Sequence[str]) -> tuple[
    Callable[[str], Any],
    Callable[[], list[str]],
    list[str],
]:
  """Lazily loads submodules of a package.

  Returns:
    A tuple of ``__getattr__``, ``__dir__`` function and ``__all__`` --
    a list of available global names, which can be used to replace the
    corresponding definitions in the package.

  Raises:
    RuntimeError: If the ``__name__`` of the caller cannot be determined.
  """
  owner_name = sys._getframe(1).f_globals.get("__name__")
  if owner_name is None:
    raise RuntimeError("Cannot determine the ``__name__`` of the caller.")

  __all__ = list(submodules)

  def __getattr__(name: str) -> Any:
    if name in submodules:
      value = importlib.import_module(f"{package_name}.{name}")
      # Update module-level globals to avoid calling ``__getattr__`` again
      # for this ``name``.
      assert owner_name is not None  # pyrefly#40
      setattr(sys.modules[owner_name], name, value)
      return value
    raise AttributeError(f"module '{package_name}' has no attribute '{name}'")

  def __dir__() -> list[str]:
    return __all__

  return __getattr__, __dir__, __all__

