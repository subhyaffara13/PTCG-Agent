
def breakpoint() -> None:
    """Programmatic breakpoint for user code.

    Place this in code compiled by Dynamo. During tracing, Dynamo inserts a
    BREAKPOINT_MARKER into the compiled bytecode. When the bytecode debugger
    is active, execution pauses at this marker.
    """


def breakpoint(*, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> Breakpoint:
  return Breakpoint(loc=loc, ip=ip)


def breakpoint(*, backend: str | None = None, filter_frames: bool = True,
               num_frames: int | None = None, ordered: bool = False,
               token = None, **kwargs):
  """Enters a breakpoint at a point in a program.

  Args:
    backend: The debugger backend to use. By default, picks the highest priority
      debugger and in the absence of other registered debuggers, falls back to
      the CLI debugger.
    filter_frames: Whether or not to filter out JAX-internal stack frames from
      the traceback. Since some libraries, like Flax, also make use of JAX's
      stack frame filtering system, this option can also affect whether stack
      frames from libraries are filtered.
    num_frames: The number of frames above the current stack frame to make
      available for inspection in the interactive debugger.
    ordered: A keyword only argument used to indicate whether or not the
      staged out computation will enforce ordering of this ``jax.debug.breakpoint``
      with respect to other ordered ``jax.debug.breakpoint`` and ``jax.debug.print``
      calls.
    token: A keyword only argument; an alternative to ``ordered``. If used then a JAX
      array (or pytree of JAX arrays) should be passed, and the breakpoint will be run
      once its value is computed.
      This is returned unchanged, and should be passed back to the computation.
      If the return value is unused in the later computation, then the whole computation
      will be pruned and this breakpoint will not be run.

  Returns:
    If `token` is passed, then its value is returned unchanged. Otherwise, returns
    `None`.
  """
  if token is not None:
    if ordered:
      raise ValueError("`ordered` and `token` are mutually exclusive arguments.")
  frame_infos = inspect.stack()
  # Throw out first frame corresponding to this function
  frame_infos = frame_infos[1:]
  # Filter out internal frames
  if filter_frames:
    frames = [
        DebuggerFrame.from_frameinfo(frame_info)
        for frame_info in frame_infos
        if traceback_util.include_frame(frame_info.frame)
    ]
  else:
    frames = [
        DebuggerFrame.from_frameinfo(frame_info)
        for frame_info in frame_infos
    ]
  if num_frames is not None:
    frames = frames[:num_frames]
  flat_args, frames_tree = tree_util.tree_flatten(frames)

  def _breakpoint_callback(*flat_args):
    frames = tree_util.tree_unflatten(frames_tree, flat_args)
    thread_id = None
    if threading.current_thread() is not threading.main_thread():
      thread_id = threading.get_ident()
    debugger = get_debugger(backend=backend)
    # Lock here because this could be called from multiple threads at the same
    # time.
    with debug_lock:
      debugger(frames, thread_id, **kwargs)

  if token is None:
    debugging.debug_callback(_breakpoint_callback, *flat_args, ordered=ordered)
  else:
    def _breakpoint_callback_wrapper(x, *flat_args):
      _breakpoint_callback(*flat_args)
      return x
    token, flat_args = lax.stop_gradient((token, flat_args))
    return callback.pure_callback(_breakpoint_callback_wrapper, token, token, *flat_args)

