
def _get_severity(severity: str) -> str:
  """Gets the severity of the log message.

  Args:
    severity: The severity of the log message.

  Returns:
    The severity of the log message.
  """
  if severity == 'DEBUG':
    return 'DEBUG'
  elif severity == 'INFO':
    return 'INFO'
  elif severity == 'WARNING':
    return 'WARNING'
  elif severity == 'ERROR':
    return 'ERROR'
  elif severity == 'CRITICAL':
    return 'CRITICAL'
  else:
    return 'INFO'

