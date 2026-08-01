
def lax_named_reduce_ops():
  return [
      NamedReducerOpRecord(lax.reduce_sum, np.sum, number_dtypes),
      NamedReducerOpRecord(lax.reduce_prod, np.prod, number_dtypes),
      NamedReducerOpRecord(lax.reduce_max, np.max, all_dtypes),
      NamedReducerOpRecord(lax.reduce_min, np.min, all_dtypes),
      NamedReducerOpRecord(lax.reduce_and, np.bitwise_and.reduce,
                           bool_dtypes + int_dtypes + uint_dtypes),
      NamedReducerOpRecord(lax.reduce_or, np.bitwise_or.reduce,
                           bool_dtypes + int_dtypes + uint_dtypes),
      NamedReducerOpRecord(lax.reduce_xor, np.bitwise_xor.reduce,
                           bool_dtypes + int_dtypes + uint_dtypes),
  ]

