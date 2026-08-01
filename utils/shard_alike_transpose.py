
def shard_alike_transpose(ct, **kwargs):
  x_ct, y_ct = ct
  if type(x_ct) is ad.Zero or type(y_ct) is ad.Zero:
    return x_ct, y_ct
  else:
    return shard_alike(x_ct, y_ct)

