
def write_podspec_rule(f, rule, depth):
  """Writes podspec from given rule."""
  indent = "  " * (depth + 1)
  spec_var = get_spec_var(depth)
  # Puts all files in hdrs, textual_hdrs, and srcs into source_files.
  # Since CocoaPods treats header_files a bit differently from bazel,
  # this won't generate a header_files field so that all source_files
  # are considered as header files.
  srcs = sorted(set(rule.hdrs + rule.textual_hdrs + rule.srcs))
  write_indented_list(
      f, "{indent}{var}.source_files = ".format(indent=indent, var=spec_var),
      srcs)
  # Writes dependencies of this rule.
  for dep in sorted(rule.deps):
    name = get_spec_name(dep.replace(":", "/"))
    f.write("{indent}{var}.dependency '{dep}'\n".format(
        indent=indent, var=spec_var, dep=name))
  # Writes dependency to xcprivacy
  f.write(
      "{indent}{var}.dependency '{dep}'\n".format(
          indent=indent, var=spec_var, dep="abseil/xcprivacy"
      )
  )

