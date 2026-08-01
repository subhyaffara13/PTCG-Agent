
def _new_model() -> rcfr.DeepRcfrModel:
  return rcfr.DeepRcfrModel(
      _GAME,
      num_hidden_layers=1,
      num_hidden_units=13,
      num_hidden_factors=1,
      use_skip_connections=True,
  )


def _new_model():
  return neurd.DeepNeurdModel(
      _GAME,
      num_hidden_layers=1,
      num_hidden_units=13,
      num_hidden_factors=1,
      use_skip_connections=True,
      autoencode=True,
  )


def _new_model():
  return rcfr.DeepRcfrModel(
      _GAME,
      num_hidden_layers=1,
      num_hidden_units=13,
      num_hidden_factors=1,
      use_skip_connections=True,
  )

