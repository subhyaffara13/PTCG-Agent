
def _cached_index_calc(s, shape):
  map_ = s.addressable_devices_indices_map(shape)
  seen_h_indices = set()
  l = []
  for array_index, index in enumerate(map_.values()):
    h_index = hashed_index(index)
    if h_index not in seen_h_indices:
      seen_h_indices.add(h_index)
      l.append((array_index, index))
  return l

