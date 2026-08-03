import logging

def get_sharding_or_none(serialized_string):
  try:
    return from_serialized_string(serialized_string.item()).to_jax_sharding()
  except ValueError as e:
    logging.error(e)

