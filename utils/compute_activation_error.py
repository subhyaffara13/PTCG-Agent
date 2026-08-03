from typing import Callable

def compute_activation_error(
    activations_match: dict[str, dict[str, Sequence[numpy.ndarray]]],
    err_func: Callable[
        [Sequence[numpy.ndarray], Sequence[numpy.ndarray]], float
    ] = compute_signal_to_quantization_noice_ratio,
) -> dict[str, dict[str, float]]:
    result: dict[str, dict[str, float]] = {}
    for name, match in activations_match.items():
        err_result: dict[str, float] = {}
        err_result["qdq_err"] = err_func(match["pre_qdq"], match["post_qdq"])
        float_activation = match["float"]
        if float_activation:
            err_result["xmodel_err"] = err_func(float_activation, match["post_qdq"])
        result[name] = err_result
    return result

