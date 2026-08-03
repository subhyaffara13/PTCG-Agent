import os

def collect_rules(root_path):
  """Collects and returns all rules from root path recursively."""
  rules = []
  for cur, _, _ in os.walk(root_path):
    build_path = os.path.join(cur, "BUILD.bazel")
    if os.path.exists(build_path):
      rules.extend(read_build("//" + cur))
  return rules

