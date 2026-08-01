
def tabular_policy_to_cpp_map(policy):
  """Turns a policy into a C++ compatible bytestring for brace-initializing.

  Args:
    policy: A dict representing a tabular policy. The keys are infostate
      bytestrings.

  Returns:
    A bytestring that can be copy-pasted to brace-initialize a C++
    std::map<std::string, open_spiel::ActionsAndProbs>.
  """
  cpp_entries = []
  policy_keys = sorted(policy.keys())
  for key in policy_keys:
    tuple_strs = ["{%i, %s}" % (p[0], p[1].astype(str)) for p in policy[key]]
    value = "{" + ", ".join(tuple_strs) + "}"
    cpp_entries.append('{"%s", %s}' % (key, value))
  return "{%s}" % (",\n".join(cpp_entries))

