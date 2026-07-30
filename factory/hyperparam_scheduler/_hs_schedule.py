from . import Any, Dict, Optional, math
from .optunamctstuner import OptunaMCTSTuner

def _get_progress(iteration: int, total_iterations: int) -> float:
    return min(1.0, max(0.0, iteration / total_iterations))

def _get_learning_rate(lr_start: float, lr_end: float, progress: float) -> float:
    cosine_decay = 0.5 * (1.0 + math.cos(math.pi * progress))
    return lr_end + (lr_start - lr_end) * cosine_decay

def _get_entropy_coef(entropy_start: float, entropy_end: float, progress: float) -> float:
    return entropy_start + (entropy_end - entropy_start) * progress

def _get_c_puct(cpuct_start: float, cpuct_end: float, cpuct_step_interval: int, iteration: int, total_iterations: int) -> float:
    num_steps = iteration // cpuct_step_interval
    total_steps = total_iterations // cpuct_step_interval
    if total_steps <= 0: return cpuct_start
    step_size = (cpuct_start - cpuct_end) / total_steps
    return max(cpuct_end, cpuct_start - num_steps * step_size)

def _get_clip_ratio(clip_start: float, clip_end: float, progress: float) -> float:
    return clip_start + (clip_end - clip_start) * progress

def _get_mcts_params(cpuct_start: float, cpuct_end: float, cpuct_step_interval: int, iteration: Optional[int] = None, total_iterations: int = 500) -> Dict[str, Any]:
    c_puct = _get_c_puct(cpuct_start, cpuct_end, cpuct_step_interval, iteration, total_iterations) if iteration is not None else cpuct_start
    defaults = OptunaMCTSTuner.get_default_mcts_params()
    defaults["c_puct"] = c_puct
    return defaults
