
def parse_preflib_datafile(filename: str) -> base.PreferenceProfile:
  """Parses a Preflib data file.

  Currently only supports SOC and SOI. See https://www.preflib.org/format.

  Args:
    filename: the name of the file to parse.

  Returns:
    A preference profile.
  """
  contents = pyspiel.read_contents_from_file(filename, "r")
  return parse_preflib_data(contents)

