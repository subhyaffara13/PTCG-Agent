
def lax_ops():
  return [
      op_record(
          "neg", 1, default_dtypes + complex_dtypes, test_util.rand_small
      ),
      op_record("sign", 1, default_dtypes + uint_dtypes, test_util.rand_small),
      op_record("floor", 1, float_dtypes, test_util.rand_small),
      op_record("ceil", 1, float_dtypes, test_util.rand_small),
      op_record("round", 1, float_dtypes, test_util.rand_default),
      op_record(
          "nextafter",
          2,
          [f for f in float_dtypes if f != dtypes.bfloat16],
          test_util.rand_default,
          tol=0,
      ),
      op_record("is_finite", 1, float_dtypes, test_util.rand_small),
      op_record("exp", 1, float_dtypes + complex_dtypes, test_util.rand_small),
      op_record("exp2", 1, float_dtypes + complex_dtypes, test_util.rand_small),
      # TODO(b/142975473): on CPU, expm1 for float64 is only accurate to ~float32
      # precision.
      op_record(
          "expm1",
          1,
          float_dtypes + complex_dtypes,
          test_util.rand_small,
          {np.float64: 1e-8},
      ),
      op_record(
          "log", 1, float_dtypes + complex_dtypes, test_util.rand_positive
      ),
      op_record(
          "log1p", 1, float_dtypes + complex_dtypes, test_util.rand_positive
      ),
      # TODO(b/142975473): on CPU, tanh for complex128 is only accurate to
      # ~float32 precision.
      # TODO(b/143135720): on GPU, tanh has only ~float32 precision.
      op_record(
          "tanh",
          1,
          float_dtypes + complex_dtypes,
          test_util.rand_small,
          {np.float64: 1e-9, np.complex128: 1e-7},
      ),
      op_record(
          "logistic", 1, float_dtypes + complex_dtypes, test_util.rand_default
      ),
      op_record(
          "sin", 1, float_dtypes + complex_dtypes, test_util.rand_default
      ),
      op_record(
          "cos", 1, float_dtypes + complex_dtypes, test_util.rand_default
      ),
      op_record("atan2", 2, float_dtypes, test_util.rand_default),
      op_record("sqrt", 1, float_dtypes, test_util.rand_positive),
      op_record("sqrt", 1, complex_dtypes, test_util.rand_default),
      op_record("rsqrt", 1, float_dtypes, test_util.rand_positive),
      op_record("rsqrt", 1, complex_dtypes, test_util.rand_default),
      op_record("cbrt", 1, float_dtypes, test_util.rand_default),
      op_record(
          "square", 1, float_dtypes + complex_dtypes, test_util.rand_default
      ),
      op_record(
          "reciprocal",
          1,
          float_dtypes + complex_dtypes,
          test_util.rand_positive,
      ),
      op_record(
          "tan",
          1,
          float_dtypes + complex_dtypes,
          test_util.rand_default,
          {np.float32: 3e-5},
      ),
      op_record(
          "asin",
          1,
          float_dtypes + complex_dtypes,
          test_util.rand_small,
          {np.complex128: 5e-12},
      ),
      op_record("acos", 1, float_dtypes + complex_dtypes, test_util.rand_small),
      op_record("atan", 1, float_dtypes + complex_dtypes, test_util.rand_small),
      op_record(
          "asinh",
          1,
          float_dtypes + complex_dtypes,
          test_util.rand_default,
          tol={np.complex64: 1e-4, np.complex128: 1e-5},
      ),
      op_record(
          "acosh", 1, float_dtypes + complex_dtypes, test_util.rand_positive
      ),
      # TODO(b/155331781): atanh has only ~float precision
      op_record(
          "atanh",
          1,
          float_dtypes + complex_dtypes,
          test_util.rand_small,
          {np.float64: 1e-9},
      ),
      op_record(
          "sinh", 1, float_dtypes + complex_dtypes, test_util.rand_default
      ),
      op_record(
          "cosh", 1, float_dtypes + complex_dtypes, test_util.rand_default
      ),
      op_record(
          "lgamma",
          1,
          float_dtypes,
          test_util.rand_positive,
          {
              np.float32: 1e-5,
              np.float64: 1e-14,
          },
      ),
      op_record(
          "digamma",
          1,
          float_dtypes,
          test_util.rand_positive,
          {np.float64: 1e-14},
      ),
      op_record(
          "betainc",
          3,
          float_dtypes,
          test_util.rand_uniform,
          {
              np.float32: 2e-5,
              np.float64: 1e-12,
          },
      ),
      op_record(
          "igamma",
          2,
          [f for f in float_dtypes if f not in [dtypes.bfloat16, np.float16]],
          test_util.rand_positive,
          {np.float64: 1e-14},
      ),
      op_record(
          "igammac",
          2,
          [f for f in float_dtypes if f not in [dtypes.bfloat16, np.float16]],
          test_util.rand_positive,
          {np.float64: 1e-14},
      ),
      op_record("erf", 1, float_dtypes, test_util.rand_small),
      op_record("erfc", 1, float_dtypes, test_util.rand_small),
      # TODO(b/142976030): the approximation of erfinf used by XLA is only
      # accurate to float32 precision.
      op_record(
          "erf_inv", 1, float_dtypes, test_util.rand_small, {np.float64: 1e-9}
      ),
      op_record("bessel_i0e", 1, float_dtypes, test_util.rand_default),
      op_record("bessel_i1e", 1, float_dtypes, test_util.rand_default),
      op_record("real", 1, complex_dtypes, test_util.rand_default),
      op_record("imag", 1, complex_dtypes, test_util.rand_default),
      op_record("complex", 2, complex_elem_dtypes, test_util.rand_default),
      op_record(
          "conj",
          1,
          complex_elem_dtypes + complex_dtypes,
          test_util.rand_default,
      ),
      op_record(
          "abs", 1, default_dtypes + complex_dtypes, test_util.rand_default
      ),
      op_record(
          "pow", 2, float_dtypes + complex_dtypes, test_util.rand_positive
      ),
      op_record("bitwise_and", 2, bool_dtypes, test_util.rand_small),
      op_record("bitwise_not", 1, bool_dtypes, test_util.rand_small),
      op_record("bitwise_or", 2, bool_dtypes, test_util.rand_small),
      op_record("bitwise_xor", 2, bool_dtypes, test_util.rand_small),
      op_record(
          "population_count", 1, int_dtypes + uint_dtypes, test_util.rand_int
      ),
      op_record("clz", 1, int_dtypes + uint_dtypes, test_util.rand_int),
      op_record(
          "add", 2, default_dtypes + complex_dtypes, test_util.rand_small
      ),
      op_record(
          "sub", 2, default_dtypes + complex_dtypes, test_util.rand_small
      ),
      op_record(
          "mul", 2, default_dtypes + complex_dtypes, test_util.rand_small
      ),
      op_record("mulhi", 2, int_dtypes + uint_dtypes, test_util.rand_fullrange),
      op_record(
          "div", 2, default_dtypes + complex_dtypes, test_util.rand_nonzero
      ),
      op_record("rem", 2, default_dtypes, test_util.rand_nonzero),
      op_record("max", 2, all_dtypes, test_util.rand_small),
      op_record("min", 2, all_dtypes, test_util.rand_small),
      op_record("eq", 2, all_dtypes, test_util.rand_some_equal),
      op_record("ne", 2, all_dtypes, test_util.rand_small),
      op_record("ge", 2, default_dtypes, test_util.rand_small),
      op_record("gt", 2, default_dtypes, test_util.rand_small),
      op_record("le", 2, default_dtypes, test_util.rand_small),
      op_record("lt", 2, default_dtypes, test_util.rand_small),
  ]

