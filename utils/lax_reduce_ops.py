
def lax_reduce_ops():
  return [
      ReducerOpRecord(lax.add, np.add, 0, default_dtypes, lax.reduce_sum_p),
      ReducerOpRecord(
          lax.mul, np.multiply, 1, default_dtypes, lax.reduce_prod_p
      ),
      ReducerOpRecord(
          lax.max, np.maximum, 0, uint_dtypes + bool_dtypes, lax.reduce_max_p
      ),
      ReducerOpRecord(
          lax.max, np.maximum, -np.inf, float_dtypes, lax.reduce_max_p
      ),
      ReducerOpRecord(
          lax.max,
          np.maximum,
          dtypes.iinfo(np.int32).min,
          [np.int32],
          lax.reduce_max_p,
      ),
      ReducerOpRecord(
          lax.max,
          np.maximum,
          dtypes.iinfo(np.int64).min,
          [np.int64],
          lax.reduce_max_p,
      ),
      ReducerOpRecord(
          lax.min, np.minimum, np.inf, float_dtypes, lax.reduce_min_p
      ),
      ReducerOpRecord(
          lax.min,
          np.minimum,
          dtypes.iinfo(np.int32).max,
          [np.int32],
          lax.reduce_min_p,
      ),
      ReducerOpRecord(
          lax.min,
          np.minimum,
          dtypes.iinfo(np.int64).max,
          [np.int64],
          lax.reduce_min_p,
      ),
      ReducerOpRecord(
          lax.min,
          np.minimum,
          dtypes.iinfo(np.uint32).max,
          [np.uint32],
          lax.reduce_min_p,
      ),
      ReducerOpRecord(
          lax.min,
          np.minimum,
          dtypes.iinfo(np.uint64).max,
          [np.uint64],
          lax.reduce_min_p,
      ),
      ReducerOpRecord(
          lax.bitwise_and,
          np.bitwise_and,
          -1,
          int_dtypes + uint_dtypes + bool_dtypes,
          lax.reduce_and_p,
      ),
      ReducerOpRecord(
          lax.bitwise_or,
          np.bitwise_or,
          0,
          int_dtypes + uint_dtypes + bool_dtypes,
          lax.reduce_or_p,
      ),
      ReducerOpRecord(
          lax.bitwise_xor,
          np.bitwise_xor,
          0,
          int_dtypes + uint_dtypes + bool_dtypes,
          lax.reduce_xor_p,
      ),
  ]

