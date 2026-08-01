
def api_selector(api_version):
  """Allows to choose an implementation API.

  Args:
    api_version (str): either of {AVIALABLE_APIS}

  Returns:
    model_lib: the model library with the chosen API.

  Raises:
    ValueError: if the user used smth different
  """
  if api_version == "nnx":
    from open_spiel.python.algorithms.alpha_zero import model_nnx as model_lib
  elif api_version == "linen":
    from open_spiel.python.algorithms.alpha_zero import model_linen as model_lib
  else:
    raise ValueError(f"Only {AVIALABLE_APIS} APIs are implmented")

  return model_lib

