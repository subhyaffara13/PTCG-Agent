
def write_indented_list(f, leading, values):
  """Writes leading values in an indented style."""
  f.write(leading)
  f.write((",\n" + " " * len(leading)).join("'{}'".format(v) for v in values))
  f.write("\n")

