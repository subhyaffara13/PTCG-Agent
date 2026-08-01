
def replay(filename: str) -> None:
    from .backends.debugging import eager

    original_replay_val = config.replay_record_enabled
    config.replay_record_enabled = False
    with open(filename, "rb") as in_file:
        record = ExecutionRecord.load(in_file)
    record.globals = dict(itertools.chain(record.globals.items(), globals().items()))

    with decorators.error_on_graph_break(False):
        try:
            _compile(
                record.code,
                record.globals,
                record.locals,
                record.builtins,
                record.closure,
                compiler_fn=eager,
                one_graph=False,
                export=False,
                export_constraints=None,
                hooks=Hooks(),
                cache_size=CacheSizeRelevantForFrame(0, 0),
                cache_entry=None,
                frame=None,
                frame_state={},
                compile_id=CompileId(frame_id=42, frame_compile_id=999),
            )
        finally:
            config.replay_record_enabled = original_replay_val


def replay(filename):
  """Re-runs the playthrough in the specified file. Returns (original, new)."""
  original, kwargs = _read_playthrough(filename)
  return (original, playthrough(**kwargs))

