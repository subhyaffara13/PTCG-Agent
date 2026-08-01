
def set_verbose() -> None:
  """Log stderr & `absl.logging` in Colab (filtered by default)."""
  # pylint: disable=g-import-not-at-top
  # pytype: disable=import-error
  from absl import logging
  from colabtools import googlelog
  # pytype: enable=import-error
  # pylint: enable=g-import-not-at-top

  logging.set_verbosity(logging.INFO)
  googlelog.set_global_capture(True)

  # See:
  # https://docs.python.org/3/library/warnings.html#overriding-the-default-filter
  if not sys.warnoptions:
    warnings.simplefilter('default')
    os.environ['PYTHONWARNINGS'] = 'default'  # Also affect subprocesses

