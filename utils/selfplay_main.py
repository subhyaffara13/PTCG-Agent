
def selfplay_main(argv):
  """Self play."""
  del argv
  np.random.seed(FLAGS.seed)
  # rock-paper-scissor
  base_matrix = np.array([[[0, -1, 1], [1, 0, -1], [-1, 1, 0]]] *
                         FLAGS.batch_size)
  dataset = matrix_dataset.Dataset(
      base_matrix=base_matrix,
      num_training_batches=FLAGS.num_batches,
      minval=FLAGS.min_val,
      maxval=FLAGS.max_val)
  data_loader = dataset.get_training_batch()
  eval_payoff_batch = dataset.get_eval_batch()

  mr_agent = meta_selfplay_agent.MetaSelfplayAgent(
      repeats=FLAGS.repeats,
      training_epochs=FLAGS.evaluation_steps,
      data_loader=data_loader)
  mr_agent.train()

  mr_agent2 = meta_selfplay_agent.MetaSelfplayAgent(
      repeats=FLAGS.repeats,
      training_epochs=FLAGS.evaluation_steps,
      data_loader=data_loader)
  mr_agent2.train()

  rm_agent = regret_matching_agent.RegretMatchingAgent(
      num_actions=FLAGS.num_actions, data_loader=data_loader)
  rm_agent.train()

  rm_agent2 = regret_matching_agent.RegretMatchingAgent(
      num_actions=FLAGS.num_actions, data_loader=data_loader)
  rm_agent2.train()

  print("Regret matching")
  evaluation.evaluate_in_selfplay(
      agent_x=rm_agent,
      agent_y=rm_agent2,
      payoff_batch=eval_payoff_batch,
      steps_count=FLAGS.evaluation_steps)

  print("Meta regret matching")
  evaluation.evaluate_in_selfplay(
      agent_x=mr_agent,
      agent_y=mr_agent2,
      payoff_batch=eval_payoff_batch,
      steps_count=FLAGS.evaluation_steps)

