
def use_python_logging(quiet=False):
  """Uses the python implementation of the logging code.

  Args:
    quiet: No logging message about switching logging type.
  """
  get_absl_handler().activate_python_handler()
  if not quiet:
    info('Restoring pure python logging')

