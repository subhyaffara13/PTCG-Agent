
def _get_metadata(dist: Distribution | None = None):
    return message_from_string(_get_pkginfo(dist or _makedist()))


def _get_metadata(arr: jax.Array, local_shape: Shape):
  return {
      'compressor': {'id': 'zstd'},
      'shape': arr.shape,
      'chunks': np.array(np.maximum(1, local_shape)),
  }

