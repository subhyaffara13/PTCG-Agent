
def io_callback_abstract_eval(
    *avals,
    callback: _FlatCallback,
    result_avals,
    sharding: Sharding | None,
    ordered: bool,
):
  del avals, sharding, callback
  effect = _OrderedIOEffect if ordered else _IOEffect
  return result_avals, {effect}

