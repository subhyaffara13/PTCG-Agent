
def _register_and_parse_flags_with_usage(
    argv=None,
    flags_parser=parse_flags_with_usage,
):
  """Registers help flags, parses arguments and shows usage if appropriate.

  This also calls sys.exit(0) if flag --only_check_args is True.

  Args:
    argv: [str], a non-empty list of the command line arguments including
      program name, sys.argv is used if None.
    flags_parser: Callable[[List[str]], Any], the function used to parse flags.
      The return value of this function is passed to `main` untouched. It must
      guarantee FLAGS is parsed after this function is called.

  Returns:
    The return value of `flags_parser`. When using the default `flags_parser`,
    it returns the following:
    [str], a non-empty list of remaining command line arguments after parsing
    flags, including program name.

  Raises:
    Error: Raised when flags_parser is called, but FLAGS is not parsed.
    SystemError: Raised when it's called more than once.
  """
  # fmt: on
  if _register_and_parse_flags_with_usage.done:
    raise SystemError('Flag registration can be done only once.')

  define_help_flags()

  original_argv = sys.argv if argv is None else argv
  args_to_main = flags_parser(original_argv)
  if not FLAGS.is_parsed():
    raise Error('FLAGS must be parsed after flags_parser is called.')

  # Exit when told so.
  if FLAGS.only_check_args:
    sys.exit(0)
  # Immediately after flags are parsed, bump verbosity to INFO if the flag has
  # not been set.
  if FLAGS['verbosity'].using_default_value:
    FLAGS.verbosity = 0
  _register_and_parse_flags_with_usage.done = True

  return args_to_main

