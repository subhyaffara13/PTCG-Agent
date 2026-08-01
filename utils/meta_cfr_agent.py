
def meta_cfr_agent(game_name='kuhn_poker'):
  return meta_learning.MetaCFRRegretAgent(
      training_epochs=1,
      meta_learner_training_epochs=1,
      game_name=game_name,
      game_config={'players': 2},
      perturbation=False,
      seed=0,
      model_type='MLP',
      best_response=True)

