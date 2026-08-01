
def build_model(api_version: str, game):
  return utils.api_selector(api_version).Model.build_model(
      "mlp",
      game.observation_tensor_shape(),
      game.num_distinct_actions(),
      nn_width=64,
      nn_depth=2,
      weight_decay=1e-4,
      learning_rate=0.01,
      path=None,
  )


def build_model() -> nnx.Module | linen.Module:
  """Builds a model."""
  game = pyspiel.load_game(FLAGS.game)

  config = {}
  if FLAGS.config_path is not None and os.path.exists(FLAGS.config_path):
    with open(FLAGS.config_path, "r") as f:
      config = json.load(f)

  model = utils.api_selector(
      config.get("nn_api_version", FLAGS.nn_api_version)
  ).Model.build_model(
      config.get("nn_model", FLAGS.nn_model),
      game.observation_tensor_shape(),
      game.num_distinct_actions(),
      config.get("nn_width", FLAGS.nn_width),
      config.get("nn_depth", FLAGS.nn_depth),
      config.get("weight_decay", FLAGS.weight_decay),
      config.get("learning_rate", FLAGS.learning_rate),
      config.get("path", FLAGS.path),
  )

  if FLAGS.checkpoint_step is not None:
    model.load_checkpoint(FLAGS.checkpoint_step)

  return model


def build_model(game: Any, api_version: str, model_type: str):
  return utils.api_selector(api_version).Model.build_model(
      model_type,
      game.observation_tensor_shape(),
      game.num_distinct_actions(),
      nn_width=32,
      nn_depth=2,
      weight_decay=1e-4,
      learning_rate=0.01,
      path=None,
  )

