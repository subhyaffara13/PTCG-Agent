
def reset_frame_count() -> None:
    global curr_frame
    cumulative_time_spent_ns.clear()
    compilation_time_metrics.clear()
    curr_frame = 0

