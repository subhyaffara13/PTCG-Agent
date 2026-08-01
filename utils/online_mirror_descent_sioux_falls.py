
def online_mirror_descent_sioux_falls(mfg_game,
                                      number_of_iterations,
                                      md_p=None):
  nash_conv_dict = {}
  md = md_p if md_p else mirror_descent.MirrorDescent(mfg_game)
  tick_time = time.time()
  for i in range(number_of_iterations):
    md.iteration()
    md_policy = md.get_policy()
    nash_conv_md = nash_conv_module.NashConv(mfg_game, md_policy)
    nash_conv_dict[i] = nash_conv_md.nash_conv()
    print((f"Iteration {i}, Nash conv: {nash_conv_md.nash_conv()}, "
           "time: {time.time() - tick_time}"))
  timing = time.time() - tick_time
  md_policy = md.get_policy()
  distribution_mfg = distribution_module.DistributionPolicy(mfg_game, md_policy)
  policy_value_ = policy_value.PolicyValue(
      mfg_game, distribution_mfg, md_policy).value(mfg_game.new_initial_state())
  nash_conv_md = nash_conv_module.NashConv(mfg_game, md_policy)
  return timing, md_policy, nash_conv_md, policy_value_, md, nash_conv_dict

