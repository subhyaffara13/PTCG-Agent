
def _bcoo_dot_general_sampled_abstract_eval(A, B, indices, *, dimension_numbers):
  dbg = api_util.debug_info("bcoo_dot_general_sampled_abstract_eval",
                            lax.dot_general, (A, B), {})
  dense_result, = pe.abstract_eval_fun(lambda *args: [lax.dot_general(*args, dimension_numbers=dimension_numbers)], A, B,
                                       debug_info=dbg)
  dbg = api_util.debug_info("bcoo_dot_general_sampled_abstract_eval",
                            _bcoo_extract, (indices, dense_result), {})
  sparse_result, = pe.abstract_eval_fun(lambda *args: [_bcoo_extract(*args)], indices, dense_result,
                                        debug_info=dbg)
  return sparse_result

