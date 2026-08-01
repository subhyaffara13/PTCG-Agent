
def smooth(data, count):
  for k in data.keys():
    if not isinstance(k, str) or not k.startswith("time_"):
      data[k] = data[k].rolling(max(1, len(data) // count)).mean()
  return data

