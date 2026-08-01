
def double(x):
    return 2 * x


def double(x):
    return 2 * x


def double(x):
    return 2 * x


def double(x):
  return pl.pallas_call(double_kernel, out_shape=x)(x)

