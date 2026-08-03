import sys

def _lazy_import(fullname):
    """Return a lazily imported proxy for a module or library.

    Warning
    -------
    Importing using this function can currently cause trouble
    when the user tries to import from a subpackage of a module before
    the package is fully imported. In particular, this idiom may not work:

      np = lazy_import("numpy")
      from numpy.lib import recfunctions

    This is due to a difference in the way Python's LazyLoader handles
    subpackage imports compared to the normal import process. Hopefully
    we will get Python's LazyLoader to fix this, or find a workaround.
    In the meantime, this is a potential problem.

    The workaround is to import numpy before importing from the subpackage.

    Notes
    -----
    We often see the following pattern::

      def myfunc():
          import scipy as sp
          sp.argmin(...)
          ....

    This is to prevent a library, in this case `scipy`, from being
    imported at function definition time, since that can be slow.

    This function provides a proxy module that, upon access, imports
    the actual module.  So the idiom equivalent to the above example is::

      sp = lazy.load("scipy")

      def myfunc():
          sp.argmin(...)
          ....

    The initial import time is fast because the actual import is delayed
    until the first attribute is requested. The overall import time may
    decrease as well for users that don't make use of large portions
    of the library.

    Parameters
    ----------
    fullname : str
        The full name of the package or subpackage to import.  For example::

          sp = lazy.load("scipy")  # import scipy as sp
          spla = lazy.load("scipy.linalg")  # import scipy.linalg as spla

    Returns
    -------
    pm : importlib.util._LazyModule
        Proxy module. Can be used like any regularly imported module.
        Actual loading of the module occurs upon first attribute request.

    """
    try:
        return sys.modules[fullname]
    except:
        pass

    # Not previously loaded -- look it up
    spec = importlib.util.find_spec(fullname)

    if spec is None:
        try:
            parent = inspect.stack()[1]
            frame_data = {
                "spec": fullname,
                "filename": parent.filename,
                "lineno": parent.lineno,
                "function": parent.function,
                "code_context": parent.code_context,
            }
            return DelayedImportErrorModule(frame_data, "DelayedImportErrorModule")
        finally:
            del parent

    module = importlib.util.module_from_spec(spec)
    sys.modules[fullname] = module

    loader = importlib.util.LazyLoader(spec.loader)
    loader.exec_module(module)

    return module


def _lazy_import() -> None:
    from .. import backends
    from ..utils import import_submodule

    import_submodule(backends)

    from ..repro.after_dynamo import dynamo_minifier_backend

    assert dynamo_minifier_backend is not None

    _discover_entrypoint_backends()


def _lazy_import(
    name: str,
    globals_=None,
    locals_=None,
    fromlist: tuple[str, ...] = (),
    level: int = 0,
):
  """Mock of `builtins.__import__`."""
  del globals_, locals_  # Unused
  if level:
    raise ValueError(f'Relative import statements not supported ({name}).')

  root_name, *parts = name.split('.')
  root = _ModuleImportProxy(name=root_name)

  # Extract inner-most module
  child = root
  for name in parts:
    child = getattr(child, name)

  if fromlist:
    # from x.y.z import a, b
    return child  # return the inner-most module (`x.y.z`)
  else:
    # import x.y.z
    # import x.y.z as z
    return root  # return the top-level module (`x`)


def _lazy_import(
    name: str,
    globals_=None,
    locals_=None,
    fromlist: tuple[str, ...] = (),
    level: int = 0,
    *,
    error_callback: str | _ErrorCallback | None,
    success_callback: _SuccessCallback | None,
):
  """Mock of `builtins.__import__`."""
  del globals_, locals_  # Unused

  if level:
    raise ValueError(f"Relative import statements not supported ({name}).")

  root_name, *parts = name.split(".")
  root = LazyModule(
      module_name=root_name,
      adhoc_kwargs=curr_args.get_curr_adhoc_kwargs(),
      error_callback=error_callback,
      success_callback=success_callback,
  )

  # Extract inner-most module
  child = root
  for name in parts:
    child = _register_submodule(child, name)

  if fromlist:
    # from x.y.z import a, b

    for fl in fromlist:
      _register_submodule(child, fl)

    return child  # return the inner-most module (`x.y.z`)
  else:
    # import x.y.z
    # import x.y.z as z
    return root  # return the top-level module (`x`)

