
def write_podspec_map(f, cur_map, depth):
  """Writes podspec from rule map recursively."""
  for key, value in sorted(cur_map.items()):
    indent = "  " * (depth + 1)
    f.write("{indent}{var0}.subspec '{key}' do |{var1}|\n".format(
        indent=indent,
        key=key,
        var0=get_spec_var(depth),
        var1=get_spec_var(depth + 1)))
    if isinstance(value, dict):
      write_podspec_map(f, value, depth + 1)
    else:
      write_podspec_rule(f, value, depth + 1)
    f.write("{indent}end\n".format(indent=indent))

