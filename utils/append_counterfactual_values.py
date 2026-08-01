
def append_counterfactual_values(
    infostates: List[typing.InfostateNode],
    counterfactual_values: Dict[str, List[List[float]]]):
  for infostate in infostates:
    counterfactual_values[infostate.infostate_string].append([
        infostate.counterfactual_action_values[a]
        for a in infostate.get_actions()
    ])

