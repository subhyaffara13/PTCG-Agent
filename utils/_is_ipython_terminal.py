import sys

def _is_ipython_terminal() -> bool:
  """Returns True if running in a IPython terminal/XManager CLI environment."""
  # XManager CLI trigger binary imports

  # `epy` is imported before the `runpy.run_module(`, so main is still the
  # XManager binary
  # On Colab, `__main__.__file__` do not exists.
  main_file = getattr(__main__, '__file__', None)
  if main_file and main_file.endswith('xmanager2/client/cli/xm_cli.py'):
    return True

  # In case `epy` is imported after the XManager CLI, detecting we're in
  # `xmanager launch` is non-trivial because the script is launched with
  # `runpy.run_module(`, hiding some XManager internals and overwriting
  # `__main__`.
  if any(flag.startswith('--xm_launch_script=') for flag in sys.argv):
    return True

  if IPython := sys.modules.get('IPython'):  # pylint: disable=invalid-name
    ipython = IPython.get_ipython()
    if ipython and type(ipython).__name__ == 'TerminalInteractiveShell':
      return True
  return False

