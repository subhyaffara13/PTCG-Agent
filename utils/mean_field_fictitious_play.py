import time

def mean_field_fictitious_play(mfg_game,
                               number_of_iterations,
                               compute_metrics=False):
  fp = mean_field_fictitious_play_module.FictitiousPlay(mfg_game)
  tick_time = time.time()
  for _ in range(number_of_iterations):
    fp.iteration()
  timing = time.time() - tick_time
  fp_policy = fp.get_policy()
  # print('learning done')
  if compute_metrics:
    distribution_mfg = distribution_module.DistributionPolicy(
        mfg_game, fp_policy)
    # print('distribution done')
    policy_value_ = policy_value.PolicyValue(mfg_game, distribution_mfg,
                                             fp_policy).value(
                                                 mfg_game.new_initial_state())
    nash_conv_fp = nash_conv_module.NashConv(mfg_game, fp_policy)
    return timing, fp_policy, nash_conv_fp, policy_value_
  return timing, fp_policy

