
def lax_out_dtype_ops():
  return [
      op_record(
          "mul", 2, default_dtypes + complex_dtypes, test_util.rand_small
      ),
  ]

