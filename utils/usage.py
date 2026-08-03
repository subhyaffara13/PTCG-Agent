import sys

def usage(shorthelp=False, writeto_stdout=False, detailed_error=None,
          exitcode=None):
  """Writes __main__'s docstring to stderr with some help text.

  Args:
    shorthelp: bool, if True, prints only flags from the main module,
        rather than all flags.
    writeto_stdout: bool, if True, writes help message to stdout,
        rather than to stderr.
    detailed_error: str, additional detail about why usage info was presented.
    exitcode: optional integer, if set, exits with this status code after
        writing help.
  """
  if writeto_stdout:
    stdfile = sys.stdout
  else:
    stdfile = sys.stderr

  doc = sys.modules['__main__'].__doc__
  if not doc:
    doc = '\nUSAGE: %s [flags]\n' % sys.argv[0]
    doc = flags.text_wrap(doc, indent='       ', firstline_indent='')
  else:
    # Replace all '%s' with sys.argv[0], and all '%%' with '%'.
    num_specifiers = doc.count('%') - 2 * doc.count('%%')
    try:
      doc %= (sys.argv[0],) * num_specifiers
    except (OverflowError, TypeError, ValueError):
      # Just display the docstring as-is.
      pass
  if shorthelp:
    flag_str = FLAGS.main_module_help()
  else:
    flag_str = FLAGS.get_help()
  try:
    stdfile.write(doc)
    if flag_str:
      stdfile.write('\nflags:\n')
      stdfile.write(flag_str)
    stdfile.write('\n')
    if detailed_error is not None:
      stdfile.write('\n%s\n' % detailed_error)
  except OSError as e:
    # We avoid printing a huge backtrace if we get EPIPE, because
    # "foo.par --help | less" is a frequent use case.
    if e.errno != errno.EPIPE:
      raise
  if exitcode is not None:
    sys.exit(exitcode)


def usage():
    print("Press R, G, B to increase the color channel values,")
    print("1-9 to set the step range for the increment,")
    print("A - ADD, S- SUB, M- MULT, - MIN, + MAX")
    print("  to change the blend modes")


def usage():
    print("press keys 1-5 to change image to blit.")
    print("A - ADD, S- SUB, M- MULT, - MIN, + MAX")
    print("T - timing test for special blend modes.")


def usage():
    print("--input [device_id] : Midi message logger")
    print("--output [device_id] : Midi piano keyboard")
    print("--list : list available midi devices")


def usage():
    print("Press the 'g' key to get all of the current clipboard data")
    print("Press the 'p' key to put a string into the clipboard")
    print("Press the 'a' key to get a list of the currently available types")
    print("Press the 'i' key to put an image into the clipboard")


def usage():
    print("usage:", __usage__, file=sys.stderr)
    print("Try fonttools subset --help for more information.\n", file=sys.stderr)

