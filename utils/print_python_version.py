
def print_python_version() -> None:
  # Having this in the test output logs by default helps debugging when all
  # you've got is the log and no other idea of which Python was used.
  sys.stderr.write('Running tests under Python {0[0]}.{0[1]}.{0[2]}: '
                   '{1}\n'.format(
                       sys.version_info,
                       sys.executable if sys.executable else 'embedded.'))

