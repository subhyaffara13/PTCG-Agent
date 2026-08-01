
def parse_flags_with_usage(args):
  """Tries to parse the flags, print usage, and exit if unparsable.

  Args:
    args: [str], a non-empty list of the command line arguments including
        program name.

  Returns:
    [str], a non-empty list of remaining command line arguments after parsing
    flags, including program name.
  """
  try:
    return FLAGS(args)
  except flags.Error as error:
    message = str(error)
    if '\n' in message:
      final_message = 'FATAL Flags parsing error:\n%s\n' % textwrap.indent(
          message, '  ')
    else:
      final_message = 'FATAL Flags parsing error: %s\n' % message
    sys.stderr.write(final_message)
    sys.stderr.write('Pass --helpshort or --helpfull to see help on flags.\n')
    sys.exit(1)

