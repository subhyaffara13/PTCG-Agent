
def build_rule_directory(rules):
  """Builds a tree-style rule directory from given rules."""
  rule_dir = {}
  for rule in rules:
    cur = rule_dir
    for frag in get_spec_name(rule.package).split("/"):
      cur = cur.setdefault(frag, {})
    cur[rule.name] = rule
  return rule_dir

