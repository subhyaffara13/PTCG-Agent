
def update_vector_clock(x: VectorClock, y: VectorClock):
  x[:] = np.maximum(x[:], y[:])

