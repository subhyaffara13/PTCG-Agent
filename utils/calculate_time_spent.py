
def calculate_time_spent() -> dict[str, float]:
    total_by_key = {}
    for phase, timing in cumulative_time_spent_ns.items():
        total_by_key[phase] = timing / 1e9

    total_by_key["total_wall_time"] = total_by_key.get(
        "entire_frame_compile", 0
    ) + total_by_key.get("entire_backward_compile", 0)
    return total_by_key

