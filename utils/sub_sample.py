
def sub_sample(data, count):
  return data[:: (max(1, len(data) // count))]

