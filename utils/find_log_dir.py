
def find_log_dir(log_dir=None):
  """Returns the most suitable directory to put log files into.

  Args:
    log_dir: str|None, if specified, the logfile(s) will be created in that
      directory.  Otherwise if the --log_dir command-line flag is provided, the
      logfile will be created in that directory.  Otherwise the logfile will be
      created in a standard location.

  Raises:
    FileNotFoundError: raised when it cannot find a log directory.
  """
  # Get a list of possible log dirs (will try to use them in order).
  # NOTE: Google's internal implementation has a special handling for Google
  # machines, which uses a list of directories. Hence the following uses `dirs`
  # instead of a single directory.
  if log_dir:
    # log_dir was explicitly specified as an arg, so use it and it alone.
    dirs = [log_dir]
  elif FLAGS['log_dir'].value:
    # log_dir flag was provided, so use it and it alone (this mimics the
    # behavior of the same flag in logging.cc).
    dirs = [FLAGS['log_dir'].value]
  else:
    dirs = [tempfile.gettempdir()]

  # Find the first usable log dir.
  for d in dirs:
    if os.path.isdir(d) and os.access(d, os.W_OK):
      return d
  raise FileNotFoundError(
      "Can't find a writable directory for logs, tried %s" % dirs)

