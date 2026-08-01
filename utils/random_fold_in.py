
def random_fold_in(keys, msgs):
  msgs = jnp.asarray(msgs)
  keys, msgs = core.auto_insert_reshard(keys, msgs)
  return random_fold_in_p.bind(keys, msgs)

