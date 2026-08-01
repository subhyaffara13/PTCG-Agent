
def _maybe_better_error(self, type_, value, traceback, tb_offset=None):
  """Update the error message."""

  if (
      isinstance(value, NameError)  # isinstance to supports `epy.reraise`
      and len(value.args) == 1
      and _is_from_invalidate_module(value)
  ):
    (msg,) = value.args
    value.args = tuple([
        msg
        + "\nYou're trying to use an object created with an old version of a"
        ' module you reloaded. Please re-create the object with the reloaded'
        ' module.'
    ])
  self.showtraceback(
      (type_, value, traceback),
      tb_offset=tb_offset,
  )

