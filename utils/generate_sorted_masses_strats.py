
def generate_sorted_masses_strats(pi_list, curr_alpha_idx, strats_to_go):
  """Generates a sorted list of (mass, strats) tuples.

  Args:
    pi_list: List of stationary distributions, pi
    curr_alpha_idx: Index in alpha_list for which to start clustering
    strats_to_go: List of strategies that still need to be ordered

  Returns:
    Sorted list of (mass, strats) tuples.
  """
  if curr_alpha_idx > 0:
    sorted_masses_strats = list()
    masses_to_strats = utils.cluster_strats(pi_list[curr_alpha_idx,
                                                    strats_to_go])

    for mass, strats in sorted(masses_to_strats.items(), reverse=True):
      if len(strats) > 1:
        to_append = generate_sorted_masses_strats(pi_list, curr_alpha_idx - 1,
                                                  strats)

        to_append = [(mass, [strats_to_go[s]
                             for s in strats_list])
                     for (mass, strats_list) in to_append]

        sorted_masses_strats.extend(to_append)
      else:
        sorted_masses_strats.append((mass, [
            strats_to_go[strats[0]],
        ]))

    return sorted_masses_strats
  else:
    to_return = sorted(
        utils.cluster_strats(pi_list[curr_alpha_idx, strats_to_go]).items(),
        reverse=True)
    to_return = [(mass, [strats_to_go[s]
                         for s in strats_list])
                 for (mass, strats_list) in to_return]
    return to_return

