
def get_command_stderr(command, env=None, close_fds=True):
  """Runs the given shell command and returns a tuple.

  Args:
    command: List or string representing the command to run.
    env: Dictionary of environment variable settings. If None, no environment
        variables will be set for the child process. This is to make tests
        more hermetic. NOTE: this behavior is different than the standard
        subprocess module.
    close_fds: Whether or not to close all open fd's in the child after forking.
        On Windows, this is ignored and close_fds is always False.

  Returns:
    Tuple of (exit status, text printed to stdout and stderr by the command).
  """
  if env is None: env = {}
  if os.name == 'nt':
    # Windows does not support setting close_fds to True while also redirecting
    # standard handles.
    close_fds = False

  use_shell = isinstance(command, str)
  # Pass the shell command as stdin to /bin/sh rather than using Python's
  # behavior of passing it in as a command line argument. That can save us when
  # the shell command exceeds the maximum command line length but the actual
  # individual process invocations within it don't.
  if os.name != 'nt' and use_shell:
    stdin_input = command.encode()
    command = ['/bin/sh']
    use_shell = False
  else:
    stdin_input = None

  result = subprocess.run(
      command,
      close_fds=close_fds,
      env=env,
      shell=use_shell,
      input=stdin_input,
      stderr=subprocess.STDOUT,
      stdout=subprocess.PIPE,
      check=False,
  )
  return (result.returncode, result.stdout)

