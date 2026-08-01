
def generate_copt_file(style):
  """Creates a generated copt file using the given style object.

  Args:
    style: either StarlarkStyle() or CMakeStyle()
  """
  with open(relative_filename(style.filename()), "w") as f:
    f.write(style.docstring())
    f.write("\n")
    for var_name, arg_list in sorted(COPT_VARS.items()):
      f.write("\n")
      f.write(copt_list(var_name, arg_list, style))

