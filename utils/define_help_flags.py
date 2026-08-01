
def define_help_flags():
  """Registers help flags. Idempotent."""
  # Use a global to ensure idempotence.
  global _define_help_flags_called

  if not _define_help_flags_called:
    flags.DEFINE_flag(HelpFlag())
    flags.DEFINE_flag(HelpshortFlag())  # alias for --help
    flags.DEFINE_flag(HelpfullFlag())
    flags.DEFINE_flag(HelpXMLFlag())
    _define_help_flags_called = True

