from typing import Any, Dict, Optional

def _get_mcts_params(cpuct_start: float, cpuct_end: float, cpuct_step_interval: int, iteration: Optional[int] = None, total_iterations: int = 500) -> Dict[str, Any]:
    c_puct = _get_c_puct(cpuct_start, cpuct_end, cpuct_step_interval, iteration, total_iterations) if iteration is not None else cpuct_start
    defaults = OptunaMCTSTuner.get_default_mcts_params()
    defaults["c_puct"] = c_puct
    return defaults

