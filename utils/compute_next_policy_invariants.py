
def compute_next_policy_invariants(
    infostates: typing.InfostateMapping, all_actions: List[int],
    infostate_map: typing.InfostateMapping
) -> tuple[Dict[str, jnp.ndarray], Dict[str, List[int]]]:
  """Computes information needed to calculate next policy.

  This function computes one hot encodings of infostates and returns mappings
  from infostate strings to one hot representations of infostates as well as
  illegal actions.

  Args:
    infostates: List of infostate mappings.
    all_actions: List of actions.
    infostate_map: Mapping from infostate string to infostate.

  Returns:
    Returns mappings of infostate strings to one hot representation for
    infostates and illegal actions
  """
  one_hot_representations = {}
  illegal_actions = {}

  for (infostate_str, infostate) in infostates.items():
    if infostate.is_terminal():
      continue

    legal_actions = infostate.get_actions()

    if len(legal_actions) == 1:
      infostate.policy[infostate.get_actions()[0]] = 1
      continue
    infostate_str_one_hot = jax.nn.one_hot(infostate_map[infostate_str],
                                           len(infostates))
    one_hot_representations[infostate_str] = infostate_str_one_hot
    illegal_actions[infostate_str] = [
        i for i, a in enumerate(all_actions) if a not in legal_actions
    ]
  return one_hot_representations, illegal_actions

