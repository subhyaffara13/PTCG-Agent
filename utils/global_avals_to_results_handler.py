
def global_avals_to_results_handler(
    global_out_avals: Sequence[ShapedArray],
    shardings: Sequence[JSharding],
    committed: bool) -> ResultsHandler:
  handlers = [
      global_aval_to_result_handler(global_aval, s, committed)
      for global_aval, s in safe_zip(global_out_avals, shardings)
  ]
  return ResultsHandler(handlers, shardings, global_out_avals)

