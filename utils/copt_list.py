
def copt_list(name, arg_list, style):
  """Copt file generation."""

  make_line = lambda s: "    \"" + s + "\"" + style.separator()
  external_str_list = [make_line(s) for s in arg_list]

  return "\n".join(
      flatten(
          [style.list_introducer(name)],
          external_str_list,
          [style.list_closer()]))

