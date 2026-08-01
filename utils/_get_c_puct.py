
def _get_c_puct(cpuct_start: float, cpuct_end: float, cpuct_step_interval: int, iteration: int, total_iterations: int) -> float:
    num_steps = iteration // cpuct_step_interval
    total_steps = total_iterations // cpuct_step_interval
    if total_steps <= 0: return cpuct_start
    step_size = (cpuct_start - cpuct_end) / total_steps
    return max(cpuct_end, cpuct_start - num_steps * step_size)

