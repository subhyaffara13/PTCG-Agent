
def _transpose_one_output(linear_fun, primals):
  transpose_fun = api.linear_transpose(linear_fun, primals)
  def transposed_fun(x):
    (y,) = transpose_fun(x)
    return y
  return transposed_fun

