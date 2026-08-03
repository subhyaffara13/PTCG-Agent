import re

def write_podspec(f, rules, args):
  """Writes a podspec from given rules and args."""
  rule_dir = build_rule_directory(rules)["abseil"]
  # Write root part with given arguments
  spec = re.sub(r"\$\{(\w+)\}", lambda x: args[x.group(1)],
                SPEC_TEMPLATE).lstrip()
  f.write(spec)
  # Write all target rules
  write_podspec_map(f, rule_dir, 0)
  f.write("end\n")

