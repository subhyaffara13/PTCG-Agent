
def _set_make_fx_tracer(tracer: _MakefxTracer) -> Generator[None, None, None]:
    global _CURRENT_MAKE_FX_TRACER
    prev_tracer = _CURRENT_MAKE_FX_TRACER
    try:
        _CURRENT_MAKE_FX_TRACER = tracer
        yield
    finally:
        _CURRENT_MAKE_FX_TRACER = prev_tracer

