
def random_fold_in_impl_base(impl, base_arr, msgs, keys_shape):
  fold_in = iterated_vmap_binary_bcast(
      keys_shape, np.shape(msgs), impl.fold_in)
  return fold_in(base_arr, msgs)

