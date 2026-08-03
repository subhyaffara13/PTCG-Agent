import logging

def set_verbosity(verbosity: int) -> None:
    """
    Set the verbosity level for the 🤗 Transformers's root logger.

    Args:
        verbosity (`int`):
            Logging level, e.g., one of:

            - `transformers.logging.CRITICAL` or `transformers.logging.FATAL`
            - `transformers.logging.ERROR`
            - `transformers.logging.WARNING` or `transformers.logging.WARN`
            - `transformers.logging.INFO`
            - `transformers.logging.DEBUG`
    """

    _configure_library_root_logger()
    _get_library_root_logger().setLevel(verbosity)


def set_verbosity(v):
    if v <= 0:
        set_threshold(logging.WARN)
    elif v == 1:
        set_threshold(logging.INFO)
    elif v >= 2:
        set_threshold(logging.DEBUG)


def set_verbosity(verbosity: int) -> None:
    """
    Sets the level for the HuggingFace Hub's root logger.

    Args:
        verbosity (`int`):
            Logging level, e.g., `huggingface_hub.logging.DEBUG` and
            `huggingface_hub.logging.INFO`.
    """
    _get_library_root_logger().setLevel(verbosity)


def set_verbosity(v):
  """Sets the logging verbosity.

  Causes all messages of level <= v to be logged,
  and all messages of level > v to be silently discarded.

  Args:
    v: int|str, the verbosity level as an integer or string. Legal string values
        are those that can be coerced to an integer as well as case-insensitive
        'debug', 'info', 'warning', 'error', and 'fatal'.
  """
  try:
    new_level = int(v)
  except ValueError:
    new_level = converter.ABSL_NAMES[v.upper()]
  FLAGS.verbosity = new_level

