
def _mask_actions_impl(pipeline, actions: list, game_state: dict) -> Tuple[list, Dict[str, list]]:
    filtered = pipeline.mask_illegal(actions, game_state)
    bench = game_state.get("my_bench", [])
    bench_sigs = {}
    for i, poke in enumerate(bench):
        if isinstance(poke, dict):
            poke_id = poke.get('id', '?')
            poke_hp = poke.get('hp', '?')
            attached_len = len(poke.get('attached', []))
            bench_sigs[i] = f"{poke_id}_{poke_hp}_{attached_len}"
        else:
            bench_sigs[i] = f"unknown_{i}"
    groups = {}
    for action in filtered:
        sig = pipeline._calc_sig(action, bench_sigs, game_state)
        groups.setdefault(sig, []).append(action)
    canon = {g[0]: g for sig, g in groups.items()}
    return list(canon.keys()), canon


def _mask_actions_impl(pipeline, actions: list, game_state: dict) -> Tuple[list, Dict[str, list]]:
    filtered = pipeline.mask_illegal(actions, game_state)
    bench = game_state.get("my_bench", [])
    bench_sigs = {}
    for i, poke in enumerate(bench):
        if isinstance(poke, dict):
            poke_id = poke.get('id', '?')
            poke_hp = poke.get('hp', '?')
            attached_len = len(poke.get('attached', []))
            bench_sigs[i] = f"{poke_id}_{poke_hp}_{attached_len}"
        else:
            bench_sigs[i] = f"unknown_{i}"
    groups = {}
    for action in filtered:
        sig = pipeline._calc_sig(action, bench_sigs, game_state)
        groups.setdefault(sig, []).append(action)
    canon = {g[0]: g for sig, g in groups.items()}
    return list(canon.keys()), canon

