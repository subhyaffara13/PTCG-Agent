
def colocated_python_class(cls: type[object]) -> type[object]:
  """Creates a wrapper class that executes the given Python class methods on the same devices as the arguments.

  The wrapper class exposes the returned type's methods, and can be instantiated
  on JAX. An actual object will be instantiated on the host of the devices of
  the arguments' when a method of the wrapper instance is called for the first
  time.

  The actual object will persist while the wrapper object is alive, and will be
  destroyed asynchronously when the wrapper object is destroyed. Note that if
  the wrapper object is destroyed immediately without any method call, actual
  objects will not be created.

  Args:
    cls: The class to wrap as a colocated Python object.

  Returns:
    Wrapper class.
  """
  return wrap_class(cls, api_util.fun_sourceinfo(cls))

