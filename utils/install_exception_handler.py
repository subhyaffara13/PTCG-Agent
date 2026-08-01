
def install_exception_handler(handler):
  """Installs an exception handler.

  Args:
    handler: ExceptionHandler, the exception handler to install.

  Raises:
    TypeError: Raised when the handler was not of the correct type.

  All installed exception handlers will be called if main() exits via
  an abnormal exception, i.e. not one of SystemExit, KeyboardInterrupt,
  FlagsError or UsageError.
  """
  if not isinstance(handler, ExceptionHandler):
    raise TypeError('handler of type %s does not inherit from ExceptionHandler'
                    % type(handler))
  EXCEPTION_HANDLERS.append(handler)

