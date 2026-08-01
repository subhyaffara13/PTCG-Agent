
def set_from_dict(original, updates):
  for k in updates:
    if k not in original:
      original[k] = updates[k]
    else:
      if isinstance(updates[k], dict):
        set_from_dict(original[k], updates[k])
      else:
        original[k] = updates[k]

