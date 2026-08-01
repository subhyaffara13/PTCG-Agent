
def _buffer_callback_abstract_eval(
    *args,
    result_avals: tuple[core.ShapedArray, ...],
    has_side_effect: bool,
    **_,
):
  del args
  effects = {_BufferCallbackEffect} if has_side_effect else core.no_effects
  return result_avals, effects

