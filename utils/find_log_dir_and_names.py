import os
import sys

def find_log_dir_and_names(program_name=None, log_dir=None):
  """Computes the directory and filename prefix for log file.

  Args:
    program_name: str|None, the filename part of the path to the program that is
      running without its extension.  e.g: if your program is called
      ``usr/bin/foobar.py`` this method should probably be called with
      ``program_name='foobar`` However, this is just a convention, you can pass
      in any string you want, and it will be used as part of the log filename.
      If you don't pass in anything, the default behavior is as described in the
      example.  In python standard logging mode, the program_name will be
      prepended with ``py_`` if it is the ``program_name`` argument is omitted.
    log_dir: str|None, the desired log directory.

  Returns:
    (log_dir, file_prefix, symlink_prefix)

  Raises:
    FileNotFoundError: raised when it cannot find a log directory.
  """
  if not program_name:
    # Strip the extension (foobar.par becomes foobar, and
    # fubar.py becomes fubar). We do this so that the log
    # file names are similar to C++ log file names.
    program_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]

    # Prepend py_ to files so that python code gets a unique file, and
    # so that C++ libraries do not try to write to the same log files as us.
    program_name = 'py_%s' % program_name

  actual_log_dir = find_log_dir(log_dir=log_dir)

  try:
    username = getpass.getuser()
  except KeyError:
    # This can happen, e.g. when running under docker w/o passwd file.
    if hasattr(os, 'getuid'):
      # Windows doesn't have os.getuid
      username = str(os.getuid())
    else:
      username = 'unknown'
  hostname = socket.gethostname()
  file_prefix = '%s.%s.%s.log' % (program_name, hostname, username)

  return actual_log_dir, file_prefix, program_name

