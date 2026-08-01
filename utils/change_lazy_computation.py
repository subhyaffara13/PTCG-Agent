
def change_lazy_computation():
  """Overriding lazily computed values."""
  config = config_dict.ConfigDict()
  config.reference = 1
  config.reference_0 = config.get_ref('reference') + 10
  config.reference_1 = config.get_ref('reference') + 20
  config.reference_1_0 = config.get_ref('reference_1') + 100

  print(config.reference)  # Prints 1.
  print(config.reference_0)  # Prints 11.
  print(config.reference_1)  # Prints 21.
  print(config.reference_1_0)  # Prints 121.

  config.reference_1 = 30

  print(config.reference)  # Prints 1 (unchanged).
  print(config.reference_0)  # Prints 11 (unchanged).
  print(config.reference_1)  # Prints 30.
  print(config.reference_1_0)  # Prints 130.

