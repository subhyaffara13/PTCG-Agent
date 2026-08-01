
def split_leading_dim(x, to_dim):
  new_shape = to_dim + x.shape[1:]
  return x.reshape(new_shape)

