
def _apply_delta(ps: ParseState, actor: int, delta: int, cfg: Config) -> None:
  ps.contrib_street[actor] += delta
  ps.contrib_total[actor] += delta
  if ps.contrib_total[actor] >= cfg.starting_stacks[actor]:
    ps.contrib_total[actor] = cfg.starting_stacks[actor]
    ps.all_in[actor] = True

