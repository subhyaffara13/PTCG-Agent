from typing import Callable

def compute_weight_error(
    weights_match: dict[str, dict[str, numpy.ndarray]],
    err_func: Callable[[numpy.ndarray, numpy.ndarray], float] = compute_signal_to_quantization_noice_ratio,
) -> dict[str, float]:
    result: dict[str, float] = {}
    for weight_name, weight_match in weights_match.items():
        result[weight_name] = err_func(weight_match["float"], weight_match["dequantized"])
    return result

