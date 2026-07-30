def _score_bench_rank(action, game_state, profile, bench_size, my_hand_size):
    micro = 0
    bench_need = 0
    if profile == "setup":
        bench_need = 5
    elif profile in ("aggro_push", "closing"):
        bench_need = 2
    if bench_size >= bench_need:
        micro = 5
    elif my_hand_size < 3 and bench_size == 0:
        micro = -3
    return micro
