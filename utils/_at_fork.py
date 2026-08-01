
def _at_fork():
  warnings.warn(
    "os.fork() was called. os.fork() is incompatible with multithreaded code, "
    "and JAX is multithreaded, so this will likely lead to a deadlock.",
    RuntimeWarning, stacklevel=2)

