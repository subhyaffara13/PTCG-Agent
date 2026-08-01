
def pure_callback_abstract_eval(
    *avals,
    callback: _FlatCallback,
    result_avals,
    sharding: Sharding | None,
    vmap_method: str | None,
):
  del avals, callback, sharding, vmap_method
  return result_avals

