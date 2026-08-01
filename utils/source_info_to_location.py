
def source_info_to_location(
    ctx: HasTracebackCaches,
    primitive: core.Primitive | None,
    name_stack: source_info_util.NameStack,
    traceback: xc.Traceback | None,
) -> ir.Location:
  if config.include_full_tracebacks_in_locations.value:
    if traceback is None:
      loc = ir.Location.unknown()
    else:
      loc = _traceback_to_location(ctx, traceback)
  else:
    frame = source_info_util.user_frame(traceback)
    if frame is None:
      loc = ir.Location.unknown()
    else:
      loc = ir.Location.file(get_canonical_source_file(frame.file_name,
                                                       ctx.traceback_caches),
                             frame.start_line, frame.start_column)
  if primitive is None:
    if name_stack.stack:
      loc = ir.Location.name(str(name_stack), childLoc=loc)
  else:
    eqn_str = (
        f"{name_stack}/{primitive.name}" if name_stack.stack else primitive.name
    )
    loc = ir.Location.name(eqn_str, childLoc=loc)
    loc = ir.Location.name(f"{primitive.name}:", childLoc=loc)
  return loc

