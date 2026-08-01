
def relevant_rule(rule):
  """Returns true if a given rule is relevant when generating a podspec."""
  return (
      # cc_library only (ignore cc_test, cc_binary)
      rule.type == "cc_library" and
      # ignore empty rule
      (rule.hdrs + rule.textual_hdrs + rule.srcs) and
      # ignore test-only rule
      not rule.testonly)

