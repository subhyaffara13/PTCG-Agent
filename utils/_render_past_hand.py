
def _render_past_hand(acpc_hh: str, button_index: int, cfg: hh_utils.Config) -> str:
    key = (
        acpc_hh,
        button_index,
        cfg.seats,
        cfg.small_blind,
        cfg.big_blind,
        tuple(cfg.starting_stacks).__hash__(),
    )
    cached = _PAST_HAND_RENDER_CACHE.get(key)
    if cached is not None:
        return cached
    hh, _ = hh_utils.parse_acpc_line(
        acpc_hh,
        cfg=cfg,
        policy=hh_utils.ButtonPolicy(),
        button_index=button_index,
    )
    rendered = hh_utils.render_pokersite(hand=hh, observer_id=None, sitename="")
    _PAST_HAND_RENDER_CACHE[key] = rendered
    return rendered

