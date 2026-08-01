
def legal_actions_to_mask(legal_actions_list, num_actions):
  """Converts a list of legal actions to a mask.

  The mask has size num actions with a 1 in a legal positions.

  Args:
    legal_actions_list: the list of legal actions
    num_actions: number of actions (width of mask)

  Returns:
    legal actions mask.
  """
  legal_actions_mask = torch.zeros((len(legal_actions_list), num_actions),
                                   dtype=torch.bool)
  for i, legal_actions in enumerate(legal_actions_list):
    legal_actions_mask[i, legal_actions] = 1
  return legal_actions_mask

