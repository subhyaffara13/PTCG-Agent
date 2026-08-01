
def loc_tracebacks(
    *,
    max_depth: int | None = None,
    on_explicit_actn: OnExplicitAction = OnExplicitAction.USE_EXPLICIT,
    current_loc_actn: CurrentLocAction = CurrentLocAction.FALLBACK,
) -> Generator[None, None, None]:
    """Enables automatic traceback-based locations for MLIR operations.

    Operations created within this context will have their location
    automatically set based on the Python call stack.

    Args:
      max_depth: Maximum number of frames to include in the location.
        If None, the default limit is used.
      on_explicit_actn: Policy when an explicit loc= is passed to an op
        constructor.
        OnExplicitAction.USE_EXPLICIT (default) — use loc= as base, skip
          traceback.
        OnExplicitAction.USE_TRACEBACK — discard loc=, generate traceback.
      current_loc_actn: Policy for composing Location.current with the result.
        CurrentLocAction.FALLBACK (default) — use Location.current only as
          fallback.
        CurrentLocAction.NAMELOC_WRAP — extract NameLoc names from
          Location.current and wrap the computed location with them.
    """
    old_enabled = _globals.loc_tracebacks_enabled()
    old_limit = _globals.loc_tracebacks_frame_limit()
    old_on_explicit_actn = _globals.traceback_action_on_explicit_loc()
    old_current_loc_actn = _globals.traceback_action_on_current_loc()
    max_depth = old_limit if max_depth is None else max_depth
    try:
        _globals.set_loc_tracebacks_frame_limit(max_depth)
        _globals.set_traceback_action_on_explicit_loc(on_explicit_actn)
        _globals.set_traceback_action_on_current_loc(current_loc_actn)
        if not old_enabled:
            _globals.set_loc_tracebacks_enabled(True)
        yield
    finally:
        if not old_enabled:
            _globals.set_loc_tracebacks_enabled(False)
        _globals.set_loc_tracebacks_frame_limit(old_limit)
        _globals.set_traceback_action_on_explicit_loc(old_on_explicit_actn)
        _globals.set_traceback_action_on_current_loc(old_current_loc_actn)

