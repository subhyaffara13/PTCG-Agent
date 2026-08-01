
def get_batched_input(input_list: List[jax.Array],
                      infostate_list: List[InfostateNode],
                      illegal_action_list: List[List[int]], batch_size: int):
  """Returns list of function arguments extended to be consistent with batch size.

  Args:
    input_list: List of DeviceArrays.
    infostate_list: List of information state nodes.
    illegal_action_list: List of List of illegal actions. Each internal list
      contains illegal actions in each information state.
    batch_size: Batch size.

  Returns:
    input_list, infostate_list, and illegal_action_list with a size consistent
    with batch size (the size of returned arrays are multipliers of batch size).
  """
  items_to_sample = batch_size * (int(len(input_list) / batch_size) +
                                  1) - len(input_list)
  idx_sample = np.random.choice(len(input_list), items_to_sample)
  input_zip = np.array(
      list(zip(input_list, infostate_list, illegal_action_list)),
      dtype=object)
  input_lst_sample = input_zip[idx_sample]
  input_sample, infostate_sample, illegal_action_sample = zip(*input_lst_sample)

  input_list.extend(list(input_sample))
  infostate_list.extend(list(infostate_sample))
  illegal_action_list.extend(list(illegal_action_sample))
  return input_list, infostate_list, illegal_action_list

