
def sum_mean_per_example_function(nonbatch_arg, batch_arg1, batch_arg2):
  return {
      'per_example': per_example_function(nonbatch_arg, batch_arg1, batch_arg2),
      'sum': sum_function(nonbatch_arg, batch_arg1, batch_arg2),
      'mean': mean_function(nonbatch_arg, batch_arg1, batch_arg2),
  }

