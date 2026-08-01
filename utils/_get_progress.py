
def _get_progress(iteration: int, total_iterations: int) -> float:
    return min(1.0, max(0.0, iteration / total_iterations))

