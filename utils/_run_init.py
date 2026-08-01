
def _run_init(
    argv,
    flags_parser,
):
  """Does one-time initialization and re-parses flags on rerun."""
  if _run_init.done:
    return flags_parser(argv)
  command_name.make_process_name_useful()
  # Set up absl logging handler.
  logging.use_absl_handler()
  args = _register_and_parse_flags_with_usage(
      argv=argv,
      flags_parser=flags_parser,
  )
  if faulthandler:
    try:
      faulthandler.enable()
    except Exception:  # pylint: disable=broad-except
      # Some tests verify stderr output very closely, so don't print anything.
      # Disabled faulthandler is a low-impact error.
      pass
  _run_init.done = True
  return args

