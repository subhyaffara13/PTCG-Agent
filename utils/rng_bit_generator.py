
def rng_bit_generator(output_state: _ods_ir.Type, output: _ods_ir.Type, rng_algorithm: _Union[_Any, _ods_ir.Attribute], initial_state: _ods_ir.Value[_ods_ir.RankedTensorType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResultList:
  return RngBitGeneratorOp(output_state=output_state, output=output, rng_algorithm=rng_algorithm, initial_state=initial_state, loc=loc, ip=ip).results


def rng_bit_generator(output_state: _ods_ir.Type, output: _ods_ir.Type, rng_algorithm: _Union[_Any, _ods_ir.Attribute], initial_state: _ods_ir.Value[_ods_ir.RankedTensorType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResultList:
  return RngBitGeneratorOp(output_state=output_state, output=output, rng_algorithm=rng_algorithm, initial_state=initial_state, loc=loc, ip=ip).results


def rng_bit_generator(key, shape, dtype=np.uint32,
                      algorithm=RandomAlgorithm.RNG_DEFAULT,
                      *, out_sharding=None):
  """Stateless PRNG bit generator. Experimental and its use is discouraged.

  Returns uniformly distributed random bits with the specified shape and dtype
  (what is required to be an integer type) using the platform specific
  default algorithm or the one specified.

  It provides direct access to the RngBitGenerator primitive exposed by XLA
  (https://www.openxla.org/xla/operation_semantics#rngbitgenerator) for low
  level API access.

  Most users should use `jax.random` instead for a stable and more user
  friendly API.
  """
  shape = core.canonicalize_shape(shape)
  dtype = dtypes.check_and_canonicalize_user_dtype(dtype, 'rng_bit_generator')
  out_sharding = canonicalize_sharding(out_sharding, 'rng_bit_generator')
  if np.dtype(dtype) not in {np.dtype('uint8'), np.dtype('uint16'),
                             np.dtype('uint32'), np.dtype('uint64')}:
    raise TypeError(f'rng_bit_generator: unsupported dtype {dtype}')
  return tuple(
      rng_bit_generator_p.bind(
          key, shape=shape, dtype=dtype, algorithm=algorithm,
          out_sharding=out_sharding))

