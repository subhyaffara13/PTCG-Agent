import sys

def _better_logging() -> None:
  """Modify Python logging (internal)."""
  # If `absl.run` was not called (e.g. open source `pytest` tests)
  if not FLAGS.is_parsed():
    return
  # User explicitly set --logtostderr, use default behavior
  if FLAGS.logtostderr or FLAGS.alsologtostderr:
    return

  file_link = '{filename}:{lineno}'

  # Using cleaner, less verbose logger
  formatter = py_logging.Formatter(
      # Only display single letter level (`INFO`, `DEBUG`,... -> `I`, `D`,...)
      f'{{levelname:1.1}} {{asctime}} [{file_link}]: {{message}}',
      # Do not display date by default (take a lot of space and is almost
      # never important locally.
      # Also milliseconds feel overkill
      datefmt='%H:%M:%S',
      style='{',
  )

  # Display logs by default
  # We could also have used logging.use_python_logging() to have the correct
  # behaviour but any call to logging.use_cpp_logging(), including in any
  # imported dependency, could reset the configuration to C++ logging. By adding
  # an handler we are not subjected to that.
  python_handler = absl_logging.get_absl_handler().python_handler
  python_handler.setFormatter(formatter)
  py_logging.getLogger().addHandler(python_handler)

  if 'tqdm' in sys.modules:
    # Replace `sys.stderr` by the TQDM file
    # This avoid visual artifacts when `logging.info` is used inside
    # a `tqdm.tqdm` context.
    python_handler.setStream(TqdmStream())

