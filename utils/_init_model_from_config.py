
def _init_model_from_config(config: Config):
  return utils.api_selector(config.nn_api_version).Model.build_model(
      config.nn_model,
      config.observation_shape,
      config.output_size,
      config.nn_width,
      config.nn_depth,
      config.weight_decay,
      config.learning_rate,
      config.path,
      decouple_weight_decay=config.decouple_weight_decay,
  )

