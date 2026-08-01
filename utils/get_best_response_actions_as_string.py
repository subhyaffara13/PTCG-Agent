
def get_best_response_actions_as_string(best_response_actions):
  """Turns a dict<bytes, int> into a bytestring compatible with C++.

  i.e. the bytestring can be copy-pasted as the brace initialization for a
  {std::unordered_,std::,absl::flat_hash_}map<std::string, int>.

  Args:
    best_response_actions: A dict mapping bytes to ints.

  Returns:
    A bytestring that can be copy-pasted to brace-initialize a C++
    std::map<std::string, T>.
  """
  best_response_keys = sorted(best_response_actions.keys())
  best_response_strings = [
      "%s: %i" % (k, best_response_actions[k]) for k in best_response_keys
  ]
  return "{%s}" % (", ".join(best_response_strings))

