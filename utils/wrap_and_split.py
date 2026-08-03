import random

def wrap_and_split():
  key = random.key(42)
  result = random.split(key, 2)
  return random.key_data(result)

