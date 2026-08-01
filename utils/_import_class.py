
def _import_class(fqp: str):
    """Take a fully-qualified path and return the imported class or identifier.

    ``fqp`` is of the form "package.module.klass" or
    "package.module:subobject.klass".

    Warnings
    --------
    This can import arbitrary modules. Make sure you haven't installed any modules
    that may execute malicious code at import time.
    """
    if ":" in fqp:
        mod, name = fqp.rsplit(":", 1)
    else:
        mod, name = fqp.rsplit(".", 1)

    is_s3 = mod == "s3fs"
    mod = importlib.import_module(mod)
    if is_s3 and mod.__version__.split(".") < ["0", "5"]:
        warnings.warn(s3_msg)
    for part in name.split("."):
        mod = getattr(mod, part)

    if not isinstance(mod, type):
        raise TypeError(f"{fqp} is not a class")

    return mod


def _import_class(class_path: str) -> type[Any]:
  """Dynamically imports a class from a string path."""
  try:
    module_path, class_name = class_path.rsplit('.', 1)
    module = importlib.import_module(module_path)
    return getattr(module, class_name)
  except (ImportError, ValueError, AttributeError) as e:
    raise ImportError(f'Failed to import class {class_path}: {e}') from e

