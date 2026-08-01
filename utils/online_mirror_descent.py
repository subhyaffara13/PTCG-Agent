
def online_mirror_descent(mfg_game,
                          number_of_iterations,
                          compute_metrics=False,
                          return_policy=False,
                          md_p=None):
  md = md_p if md_p else mirror_descent.MirrorDescent(mfg_game)
  tick_time = time.time()
  for _ in range(number_of_iterations):
    md.iteration()
  timing = time.time() - tick_time
  md_policy = md.get_policy()
  if compute_metrics:
    distribution_mfg = distribution_module.DistributionPolicy(
        mfg_game, md_policy)
    # print('distribution done')
    policy_value_ = policy_value.PolicyValue(mfg_game, distribution_mfg,
                                             md_policy).value(
                                                 mfg_game.new_initial_state())
    nash_conv_md = nash_conv_module.NashConv(mfg_game, md_policy)
    if return_policy:
      return timing, md_policy, nash_conv_md, policy_value_, md
    return timing, md_policy, nash_conv_md, policy_value_
  return timing, md_policy

