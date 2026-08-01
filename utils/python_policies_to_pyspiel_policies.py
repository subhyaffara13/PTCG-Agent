
def python_policies_to_pyspiel_policies(policies):
  """Same conversion as above (list version).

  Args:
    policies: a list of python.TabularPolicy

  Returns:
    a list of pyspiel.TabularPolicy.
  """
  return [python_policy_to_pyspiel_policy(p) for p in policies]

