import functools
import itertools

def _map_coordinates(input: ArrayLike, coordinates: Sequence[ArrayLike],
                     order: int, mode: str, cval: ArrayLike) -> Array:
  input_arr = jnp.asarray(input)
  coordinate_arrs = [jnp.asarray(c) for c in coordinates]
  cval = jnp.asarray(cval, input_arr.dtype)

  if len(coordinates) != input_arr.ndim:
    raise ValueError('coordinates must be a sequence of length input.ndim, but '
                     '{} != {}'.format(len(coordinates), input_arr.ndim))

  index_fixer = _INDEX_FIXERS.get(mode)
  if index_fixer is None:
    raise NotImplementedError(
        'jax.scipy.ndimage.map_coordinates does not yet support mode {}. '
        'Currently supported modes are {}.'.format(mode, set(_INDEX_FIXERS)))

  if mode == 'constant':
    is_valid = lambda index, size: (0 <= index) & (index < size)
  else:
    is_valid = lambda index, size: True

  if order == 0:
    interp_fun = _nearest_indices_and_weights
  elif order == 1:
    interp_fun = _linear_indices_and_weights
  else:
    raise NotImplementedError(
        'jax.scipy.ndimage.map_coordinates currently requires order<=1')

  valid_1d_interpolations = []
  for coordinate, size in zip(coordinate_arrs, input_arr.shape):
    interp_nodes = interp_fun(coordinate)
    valid_interp = []
    for index, weight in interp_nodes:
      fixed_index = index_fixer(index, size)
      valid = is_valid(index, size)
      valid_interp.append((fixed_index, valid, weight))
    valid_1d_interpolations.append(valid_interp)

  outputs = []
  for items in itertools.product(*valid_1d_interpolations):
    indices, validities, weights = util.unzip3(items)
    if all(valid is True for valid in validities):
      # fast path
      contribution = input_arr[indices]
    else:
      all_valid = functools.reduce(operator.and_, validities)
      contribution = jnp.where(all_valid, input_arr[indices], cval)
    outputs.append(_nonempty_prod(weights) * contribution)  # pyrefly: ignore[bad-argument-type]
  result = _nonempty_sum(outputs)
  if dtypes.issubdtype(input_arr.dtype, np.integer):
    result = _round_half_away_from_zero(result)
  return result.astype(input_arr.dtype)

