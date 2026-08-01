
def supports_color() -> bool:
  """
  Returns True if the running system's terminal supports color, and False otherwise.
  """
  try:
    from IPython import get_ipython

    ipython_available = get_ipython() is not None
  except ImportError:
    ipython_available = False

  supported_platform = sys.platform != 'win32' or 'ANSICON' in os.environ
  is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
  return (supported_platform and is_a_tty) or ipython_available

