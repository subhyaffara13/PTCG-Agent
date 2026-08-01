
def _i0e_impl32(x: Array) -> Array:
  """
  Computes an approximation to the modified Bessel function of the first kind,
  zeroth order. The following implementation follows Cephes' F32 and F64
  implementation of i0e.
  """
  i0e_coeffs_a = np.array(
    [-1.30002500998624804212E-8, 6.04699502254191894932E-8,
     -2.67079385394061173391E-7, 1.11738753912010371815E-6,
     -4.41673835845875056359E-6, 1.64484480707288970893E-5,
     -5.75419501008210370398E-5, 1.88502885095841655729E-4,
     -5.76375574538582365885E-4, 1.63947561694133579842E-3,
     -4.32430999505057594430E-3, 1.05464603945949983183E-2,
     -2.37374148058994688156E-2, 4.93052842396707084878E-2,
     -9.49010970480476444210E-2, 1.71620901522208775349E-1,
     -3.04682672343198398683E-1, 6.76795274409476084995E-1]
  )
  i0e_coeffs_b = np.array(
    [3.39623202570838634515E-9, 2.26666899049817806459E-8,
     2.04891858946906374183E-7, 2.89137052083475648297E-6,
     6.88975834691682398426E-5, 3.36911647825569408990E-3,
     8.04490411014108831608E-1]
  )

  x = abs(x)
  half = full_like(x, 0.5)
  two = full_like(x, 2.0)
  thirty_two = full_like(x, 32.0)

  result_le_8 = evaluate_chebyshev_polynomial(half * x - two, i0e_coeffs_a)
  result_gt_8 = div(evaluate_chebyshev_polynomial(thirty_two / x - two,
                                                  i0e_coeffs_b), sqrt(x))

  return select(x <= 8.0, result_le_8, result_gt_8)

