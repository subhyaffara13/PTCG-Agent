
def get_verbosity() -> int:
    """
    Return the current level for the 🤗 Transformers's root logger as an int.

    Returns:
        `int`: The logging level.

    <Tip>

    🤗 Transformers has following logging levels:

    - 50: `transformers.logging.CRITICAL` or `transformers.logging.FATAL`
    - 40: `transformers.logging.ERROR`
    - 30: `transformers.logging.WARNING` or `transformers.logging.WARN`
    - 20: `transformers.logging.INFO`
    - 10: `transformers.logging.DEBUG`

    </Tip>"""

    _configure_library_root_logger()
    return _get_library_root_logger().getEffectiveLevel()


def get_verbosity() -> int:
    """Return the current level for the HuggingFace Hub's root logger.

    Returns:
        Logging level, e.g., `huggingface_hub.logging.DEBUG` and
        `huggingface_hub.logging.INFO`.

    > [!TIP]
    > HuggingFace Hub has following logging levels:
    >
    > - `huggingface_hub.logging.CRITICAL`, `huggingface_hub.logging.FATAL`
    > - `huggingface_hub.logging.ERROR`
    > - `huggingface_hub.logging.WARNING`, `huggingface_hub.logging.WARN`
    > - `huggingface_hub.logging.INFO`
    > - `huggingface_hub.logging.DEBUG`
    """
    return _get_library_root_logger().getEffectiveLevel()


def get_verbosity():
  """Returns the logging verbosity."""
  return FLAGS['verbosity'].value

