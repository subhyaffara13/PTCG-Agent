
def leaked_tracer_error(name: str, t, tracers: list[Tracer]) -> Exception:
  assert tracers
  why = partial(_why_alive, {id(tracers)})
  msgs = '\n\n'.join(f'{tracers[i]}{tracers[i]._origin_msg()}{why(tracers[i])}'
                     for i in range(len(tracers)))
  return Exception(f'Leaked {name} {t}. Leaked tracer(s):\n\n{msgs}\n')

